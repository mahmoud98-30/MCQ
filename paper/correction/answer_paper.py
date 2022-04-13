import cv2
import numpy as np
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from matplotlib import pyplot as plt

import paper.utlis as utlis
from paper.correction.parameters import widthImg, heightImg, rect_num, questions, choices


def answer_paper(request, StudentAnswerpaper):
    # convert image to array
    global SimgWarpColored, Simg, pts2, pts1
    s_arr = []
    All = []
    for answer_image in StudentAnswerpaper:
        # print(answer_image)
        s_array = plt.imread(str(answer_image))
        # print(s_array)
        # print('--------')
        s_arr.append(s_array)
        # print(s_arr)
        # print(type(s_arr))
        # print(len(s_arr))
        # Student Answer paper
        Simg = cv2.resize(s_array, (widthImg, heightImg))  # RESIZE IMAGE
        SimgContours = Simg.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
        SimgGray = cv2.cvtColor(Simg, cv2.COLOR_BGR2GRAY)  # CONVERT IMAGE TO GRAY SCALE
        SimgBlur = cv2.GaussianBlur(SimgGray, (5, 5), 1)  # ADD GAUSSIAN BLUR
        SimgCanny = cv2.Canny(SimgBlur, 10, 80)  # APPLY CANNY

        S_contours, hierarchy = cv2.findContours(SimgCanny, cv2.RETR_EXTERNAL,
                                                 cv2.CHAIN_APPROX_NONE)  # FIND ALL CONTOURS
        cv2.drawContours(SimgContours, S_contours, -1, (0, 255, 0), 3)  # DRAW ALL DETECTED
        SimgBigContour = Simg.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
        # print('----------------------------')
        # print(S_contours)

        SrectCon = utlis.rectContour(S_contours)  # FILTER FOR RECTANGLE CONTOURS
        # fimg = cv2.resize(SrectCon, (500, 500))
        # print(S_contours)
        # cv2.imshow("showAnswers Result", fimg)
        # cv2.waitKey(0)
        SRecNum = len(SrectCon)  # number of rectangles

        # print("Numpy Of Student Answer Rectangles:", SRecNum)

        if SRecNum == rect_num:
            StudentAnslist = []
            # print("Numpy Of Student Answer Rectangles:", SRecNum)

            for i in range(0, rect_num):
                # GET CORNER POINTS OF THE RECTANGLES
                StudentPoints = utlis.getCornerPoints(SrectCon[i])

                # THE RECTANGLE WARPING OF Student Answer
                StudentPoints = utlis.reorder(StudentPoints)  # REORDER FOR WARPING
                cv2.drawContours(SimgBigContour, StudentPoints, -1, (0, 255, 0), 20)  # DRAW THE  CONTOUR

                pts1 = np.float32(StudentPoints)  # PREPARE POINTS FOR WARP
                pts2 = np.float32(
                    [[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])  # PREPARE POINTS FOR WARP
                matrix = cv2.getPerspectiveTransform(pts1, pts2)  # GET TRANSFORMATION MATRIX
                SimgWarpColored = cv2.warpPerspective(Simg, matrix, (widthImg, heightImg))  # APPLY WARP PERSPECTIVE

                # APPLY THRESHOLD
                SimgWarpGray = cv2.cvtColor(SimgWarpColored, cv2.COLOR_BGR2GRAY)  # CONVERT TO GRAYSCALE
                SimgThresh = cv2.threshold(SimgWarpGray, 170, 255, cv2.THRESH_BINARY_INV)[1]  # APPLY THRESHOL
                # utlis.splitBoxes(SimgThresh)

                # cv2.imshow("Result", SimgThresh)
                # cv2.waitKey(0)

                Sboxes = utlis.splitBoxes(SimgThresh)  # GET INDIVIDUAL BOXES
                # cv2.countNonZero(Cboxes[4]), ) # print(cv2.countNonZero(Sboxes[1]), cv2.countNonZero(Sboxes[2]),
                # cv2.countNonZero(Sboxes[3]),cv2.countNonZero(Sboxes[4]), )

                ScountR = 0
                ScountC = 0
                StudentPixelVal = np.zeros((questions, choices))  # TO STORE THE NON ZERO VALUES OF EACH BOX

                for image in Sboxes:
                    # cv2.imshow(str(countR)+str(countC),image)
                    StotalPixels = cv2.countNonZero(image)
                    StudentPixelVal[ScountR][ScountC] = StotalPixels
                    ScountC += 1
                    if (ScountC == choices): ScountC = 0;ScountR += 1
                #     # print('--------------------------------------------')
                #     # print(StudentPixelVal)
                #
                #     # FIND THE USER ANSWERS AND PUT THEM IN A LIST
                StudentIndex = []

                for x in range(0, questions):
                    StotalArr = StudentPixelVal[x]
                    StudentIndexVal = np.where(StotalArr == np.amax(StotalArr))
                    # print(StudentIndexVal[0])
                    StudentIndex.append(StudentIndexVal[0][0])

                # print('StudentPixelVal', StudentPixelVal)

                # print('----------------------------------------')
                # print("Student Answers", StudentIndex)
                # print('----------------------------------------')
                StudentAnslist.append(StudentIndex)
            All.append(StudentAnslist)
            # print("StudentAnslist", StudentAnslist)
        # print("All", All)
        # print("Student Answers", StudentAnslist)
        # print("Student Answers", len(StudentAnslist))

        else:
            msg = _(
                'The Scan Of Student Answer Paper Is Bad.')
            messages.add_message(request, messages.WARNING, msg)

    return All, SimgWarpColored, Simg, pts1, pts2
