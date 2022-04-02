import cv2
import numpy as np
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from matplotlib import pyplot as plt

import paper.utlis as utlis
from paper.correction.parameters import rect_num, CorrectScore, questions, choices, heightImg, widthImg


def correct_paper(request, CorrectAnswerpaper):
    # convert image to array
    c_arr = plt.imread(CorrectAnswerpaper)
    # print(c_arr)

    # Correct Answer paper
    Cimg = cv2.resize(c_arr, (widthImg, heightImg))  # RESIZE IMAGE
    CimgContours = Cimg.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
    CimgGray = cv2.cvtColor(Cimg, cv2.COLOR_BGR2GRAY)  # CONVERT IMAGE TO GRAY SCALE
    CimgBlur = cv2.GaussianBlur(CimgGray, (5, 5), 1)  # ADD GAUSSIAN BLUR
    CimgCanny = cv2.Canny(CimgBlur, 10, 80)  # APPLY CANNY

    C_contours, C_hierarchy = cv2.findContours(CimgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # FIND ALL CONTOURS
    cv2.drawContours(CimgContours, C_contours, -1, (0, 255, 0), 3)  # DRAW ALL DETECTED
    CimgBigContour = Cimg.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
    # print(C_contours)
    CrectCon = utlis.rectContour(C_contours)  # FILTER FOR RECTANGLE CONTOURS

    CRecNum = len(CrectCon)  # number of rectangles

    # print("Numpy Of Correct Answer Rectangles:", CRecNum)

    if CRecNum == rect_num:
        CorrectAnslist = []
        for i in range(0, rect_num):
            # GET CORNER POINTS OF THE RECTANGLES
            CorrectPoints = utlis.getCornerPoints(CrectCon[i])

            # THE RECTANGLE WARPING OF Correct Answer
            CorrectPoints = utlis.reorder(CorrectPoints)  # REORDER FOR WARPING
            cv2.drawContours(CimgBigContour, CorrectPoints, -1, (0, 255, 0), 20)  # DRAW THE  CONTOUR

            pts1 = np.float32(CorrectPoints)  # PREPARE POINTS FOR WARP
            pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])  # PREPARE POINTS FOR WARP
            matrix = cv2.getPerspectiveTransform(pts1, pts2)  # GET TRANSFORMATION MATRIX
            CimgWarpColored = cv2.warpPerspective(Cimg, matrix, (widthImg, heightImg))  # APPLY WARP PERSPECTIVE

            # APPLY THRESHOLD
            CimgWarpGray = cv2.cvtColor(CimgWarpColored, cv2.COLOR_BGR2GRAY)  # CONVERT TO GRAYSCALE
            CimgThresh = cv2.threshold(CimgWarpGray, 170, 255, cv2.THRESH_BINARY_INV)[1]  # APPLY THRESHOL

            # cv2.imshow("Result", CimgThresh)
            # cv2.waitKey(0)

            Cboxes = utlis.splitBoxes(CimgThresh)  # GET INDIVIDUAL BOXES
            # # print(cv2.countNonZero(Cboxes[1]), cv2.countNonZero(Cboxes[2]), cv2.countNonZero(Cboxes[3]),

            CcountR = 0
            CcountC = 0
            CorrectPixelVal = np.zeros((questions, choices))  # TO STORE THE NON ZERO VALUES OF EACH BOX

            for image in Cboxes:
                # cv2.imshow(str(CcountR) + str(CcountC), image)
                # print(str(CcountR))
                # print(str(CcountC))
                cv2.waitKey(0)
                CtotalPixels = cv2.countNonZero(image)
                # print(CtotalPixels)
                CorrectPixelVal[CcountR][CcountC] = CtotalPixels
                CcountC += 1
                # print(CcountC)
                if (CcountC == choices): CcountC = 0;CcountR += 1
                # print('--------------------------------------------')
                # print(CcountR)
                # print(CorrectPixelVal)

            # FIND THE USER ANSWERS AND PUT THEM IN A LIST
            CorrectIndex = []
            for x in range(0, questions):
                CorrectArr = CorrectPixelVal[x]
                CorrectIndexVal = np.where(CorrectArr == np.amax(CorrectArr))
                # print(CorrectIndexVal[0])
                CorrectIndex.append(CorrectIndexVal[0][0])
            # print('CorrectPixelVal', CorrectPixelVal)
            # print('----------------------------------------')
            # print("Correct Answers", CorrectIndex)
            # print('----------------------------------------')
            CorrectAnslist.append(CorrectIndex)
            # print("CorrectAnslist", CorrectAnslist)

        return CorrectAnslist

    else:
        msg = _(
            'The Scan Of Correct Answer Paper Is Bad.')
        messages.add_message(request, messages.WARNING, msg)
