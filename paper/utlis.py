import cv2
import numpy as np

from paper.correction.parameters import questions, choices


# TO STACK ALL THE IMAGES IN ONE WINDOW
def stackImages(imgArray, scale, lables=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        hor_con = np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth = int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        # print(eachImgHeight)
        for d in range(0, rows):
            for c in range(0, cols):
                cv2.rectangle(ver, (c * eachImgWidth, eachImgHeight * d),
                              (c * eachImgWidth + len(lables[d][c]) * 13 + 27, 30 + eachImgHeight * d), (255, 255, 255),
                              cv2.FILLED)
                cv2.putText(ver, lables[d][c], (eachImgWidth * c + 10, eachImgHeight * d + 20),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 255), 2)
    return ver


def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))  # REMOVE EXTRA BRACKET
    # print(myPoints)
    myPointsNew = np.zeros((4, 1, 2), np.int32)  # NEW MATRIX WITH ARRANGED POINTS
    add = myPoints.sum(1)
    # print(add)
    # print(np.argmax(add))
    myPointsNew[0] = myPoints[np.argmin(add)]  # [0,0]
    myPointsNew[3] = myPoints[np.argmax(add)]  # [w,h]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]  # [w,0]
    myPointsNew[2] = myPoints[np.argmax(diff)]  # [h,0]

    return myPointsNew


def y_contour(contours):
    # Returns the Y cordinate for the contour centroid
    # sort contours up to bottom lift to right
    M = cv2.moments(contours)
    return (int(M['m01'] / M['m00']))


def rectContour(contours):
    rectCon = []
    qr = []
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        # print(area)
        # if 350 < area < 19000:
        if 10000 < area < 25000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            # print('-----------------------------')
            # print(len(approx))
            if len(approx) == 4:
                rectCon.append(i)
    # sort contours
    rectCon = sorted(rectCon, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * 3)
    # print(rectCon)
    # print('-----------------------------------------------------')
    # print(len(rectCon))
    return rectCon


def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True)  # LENGTH OF CONTOUR
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True)  # APPROXIMATE THE POLY TO GET CORNER POINTS
    return approx


def splitBoxes(img):
    rows = np.vsplit(img, 10)

    # cv2.imshow("Split Test ", rows[9])
    # cv2.imshow("Split Test ", rows[1])
    # cv2.imshow("Split Test ", rows[2])
    # cv2.imshow("Split Test ", rows[3])
    # cv2.imshow("Split Test ", rows[4])
    # cv2.imshow("Split Test ", rows[5])
    # cv2.imshow("Split Test ", rows[6])
    # cv2.imshow("Split Test ", rows[7])
    # cv2.imshow("Split Test ", rows[8])
    # cv2.imshow("Split Test ", rows[9])
    # cv2.waitKey(0)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, 4)
        for box in cols:
            boxes.append(box)
            # cv2.imshow("Split Test ", box)
            # cv2.waitKey(0)
    return boxes


def drawGrid(img, questions=5, choices=5):
    secW = int(img.shape[1] / questions)
    secH = int(img.shape[0] / choices)
    for i in range(0, 9):
        pt1 = (0, secH * i)
        pt2 = (img.shape[1], secH * i)
        pt3 = (secW * i, 0)
        pt4 = (secW * i, img.shape[0])
        cv2.line(img, pt1, pt2, (255, 255, 0), 2)
        cv2.line(img, pt3, pt4, (255, 255, 0), 2)
    fimg = cv2.resize(img, (500, 500))
    cv2.imshow("Result", fimg)
    cv2.waitKey(0)
    return img


def showAnswers(img, myIndex, grading, ans, questions=questions, choices=choices):
    secW = int(img.shape[1] / choices)
    secH = int(img.shape[0] / questions)
    # print("myIndex", myIndex)
    # print("ans", ans)
    # print("grading", grading)
    for x in range(0, questions):
        myAns = myIndex[x]
        cX = (myAns * secW) + secW // 2
        cY = (x * secH) + secH // 2
        # print("-" * 100)
        # print("cX", cX)
        # print("cY", cY)
        cv2.circle(img, (cX, cY), 50, (0, 255, 0), cv2.FILLED)  # just show corrct answer
    if grading[x] == 1:
        GreenColor = (0, 255, 0)
        # cv2.rectangle(img,(myAns*secW,x*secH),((myAns*secW)+secW,(x*secH)+secH),myColor,cv2.FILLED)
        cv2.circle(img, (cX, cY), 50, GreenColor, cv2.FILLED)
    else:
        RedColor = (0, 0, 255)
        # cv2.rectangle(img, (myAns * secW, x * secH), ((myAns * secW) + secW, (x * secH) + secH), myColor, cv2.FILLED)
        cv2.circle(img, (cX, cY), 50, RedColor, cv2.FILLED)
    #
        # CORRECT ANSWER
        # myColor = (0, 255, 0)
        # correctAns = ans[x]
        # cv2.circle(img, ((correctAns * secW) + secW // 2, (x * secH) + secH // 2),
        #            20, myColor, cv2.FILLED)

    # fimg = cv2.resize(img, (500, 500))
    # cv2.imshow("showAnswers Result", fimg)
    # cv2.waitKey(0)

    return img
