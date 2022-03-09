import cv2
import numpy as np
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from matplotlib import pyplot as plt

import paper.utlis as utlis


def chack_answer(CorrectAnswerpaper, StudentAnswerpaper):

    # the parameters
    heightImg = 1000
    widthImg = 1000
    CorrectScore = 10000
    questions = 10
    choices = 4
    rect_num = 10

    # PREPROCESSING

    # convert image to array
    c_arr = plt.imread(CorrectAnswerpaper)
    s_arr = plt.imread(StudentAnswerpaper)
    # print(CorrectAnswerpaper)
    # print(c_arr)
    # print('--------')
    # s_arr = []
    # for answer_image in StudentAnswerpaper:
    #     # print(answer_image)
    #     s_array = plt.imread(str(answer_image))
    #     print(s_array)
    #     print('--------')
    # s_arr.append(s_array)
    # print(s_arr)


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
    # ---------------------------------------------------------------------------------------------------------------------------
    # Student Answer paper
    Simg = cv2.resize(s_arr, (widthImg, heightImg))  # RESIZE IMAGE
    SimgContours = Simg.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
    SimgGray = cv2.cvtColor(Simg, cv2.COLOR_BGR2GRAY)  # CONVERT IMAGE TO GRAY SCALE
    SimgBlur = cv2.GaussianBlur(SimgGray, (5, 5), 1)  # ADD GAUSSIAN BLUR
    SimgCanny = cv2.Canny(SimgBlur, 10, 80)  # APPLY CANNY

    S_contours, hierarchy = cv2.findContours(SimgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # FIND ALL CONTOURS
    cv2.drawContours(SimgContours, S_contours, -1, (0, 255, 0), 3)  # DRAW ALL DETECTED
    SimgBigContour = Simg.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
    # print('----------------------------')
    # print(S_contours)
    SrectCon = utlis.rectContour(S_contours)  # FILTER FOR RECTANGLE CONTOURS

    SRecNum = len(SrectCon)  # number of rectangles
    CRecNum = len(CrectCon)  # number of rectangles

    print("Numpy Of Correct Answer Rectangles:", CRecNum)
    print("Numpy Of Student Answer Rectangles:", SRecNum)

    if SRecNum == CRecNum == rect_num:
        TotelScore = []
        GRADINGLIST = []
        CorrectAnslist = []
        StudentAnslist = []
        for i in range(0, rect_num):
            # GET CORNER POINTS OF THE RECTANGLES
            CorrectPoints = utlis.getCornerPoints(CrectCon[i])
            StudentPoints = utlis.getCornerPoints(SrectCon[i])

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

            # ---------------------------------------------------------------------------------------------------------------------------

            # THE RECTANGLE WARPING OF Student Answer
            StudentPoints = utlis.reorder(StudentPoints)  # REORDER FOR WARPING
            cv2.drawContours(SimgBigContour, StudentPoints, -1, (0, 255, 0), 20)  # DRAW THE  CONTOUR

            pts1 = np.float32(StudentPoints)  # PREPARE POINTS FOR WARP
            pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])  # PREPARE POINTS FOR WARP
            matrix = cv2.getPerspectiveTransform(pts1, pts2)  # GET TRANSFORMATION MATRIX
            SimgWarpColored = cv2.warpPerspective(Simg, matrix, (widthImg, heightImg))  # APPLY WARP PERSPECTIVE

            # APPLY THRESHOLD
            SimgWarpGray = cv2.cvtColor(SimgWarpColored, cv2.COLOR_BGR2GRAY)  # CONVERT TO GRAYSCALE
            SimgThresh = cv2.threshold(SimgWarpGray, 170, 255, cv2.THRESH_BINARY_INV)[1]  # APPLY THRESHOL
            # utlis.splitBoxes(SimgThresh)

            # cv2.imshow("Result", SimgThresh)
            # cv2.waitKey(0)

            Cboxes = utlis.splitBoxes(CimgThresh)  # GET INDIVIDUAL BOXES
            Sboxes = utlis.splitBoxes(SimgThresh)  # GET INDIVIDUAL BOXES
            # # print(cv2.countNonZero(Cboxes[1]), cv2.countNonZero(Cboxes[2]), cv2.countNonZero(Cboxes[3]),
            # cv2.countNonZero(Cboxes[4]), ) # print(cv2.countNonZero(Sboxes[1]), cv2.countNonZero(Sboxes[2]),
            # cv2.countNonZero(Sboxes[3]),cv2.countNonZero(Sboxes[4]), )
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
            CorrectIndex = []
            StudentIndex = []
            for x in range(0, questions):
                StotalArr = StudentPixelVal[x]
                StudentIndexVal = np.where(StotalArr == np.amax(StotalArr))
                # print(StudentIndexVal[0])
                StudentIndex.append(StudentIndexVal[0][0])

                CorrectArr = CorrectPixelVal[x]
                CorrectIndexVal = np.where(CorrectArr == np.amax(CorrectArr))
                # print(CorrectIndexVal[0])
                CorrectIndex.append(CorrectIndexVal[0][0])
            print('----------------------------------------')
            print("Correct Answers", CorrectIndex)
            print("Student Answers", StudentIndex)
            print('----------------------------------------')
            CorrectAnslist.append(CorrectIndex)
            StudentAnslist.append(StudentIndex)

        #     # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS
        #     grading = []
        #     for x in range(0, questions):
        #         if StudentIndex[x] == CorrectIndex[x]:
        #             grading.append(1)
        #         else:
        #             grading.append(0)
        #
        #     print("GRADING", grading)
        #     GRADINGLIST.append(grading)
        #
        #     score = (sum(grading) / questions) * 100  # FINAL GRADE
        #     TotelScore.append(score)
        #     print("SCORE", score)
        #
        # # print("TOTEL SCORE", TotelGRADING)
        # # print("TOTEL SCORE", TotelScore)
        #
        # PercentScore = (sum(TotelScore) / CorrectScore) * 100
        # # print("Finel SCORE", PercentScore)
        #
        # # put many list from one list ,to one list
        # TotelGRADING = [item for sublist in GRADINGLIST for item in sublist]
        # CorrectAns = [item for sublist in CorrectAnslist for item in sublist]
        # StudentAns = [item for sublist in StudentAnslist for item in sublist]
        #
        # # exoprt to excel file
        # excel_file = utlis.ExportExcel(TotelGRADING, TotelScore, PercentScore, CorrectAns, StudentAns)

    #     #  # DISPLAYING ANSWERS
    #     #  CResultImg = CimgWarpColored.copy()
    #     #  CResultImg = utlis.showAnswers(CResultImg, CorrectIndex, grading, ans)  # DRAW DETECTED ANSWERS
    #     #  utlis.drawGrid(CimgWarpColored)  # DRAW GRID
    #     #
    #     # # DISPLAYING ANSWERS
    #     #  SResultImg = SimgWarpColored.copy()
    #     #  SResultImg = utlis.showAnswers(SResultImg, StudentIndex, grading, ans)  # DRAW DETECTED ANSWERS
    #     #  utlis.drawGrid(SimgWarpColored)  # DRAW GRID
    #
    #     # imgRawDrawings = np.zeros_like(imgWarpColored)  # NEW BLANK IMAGE WITH WARP IMAGE SIZE
    #     # utlis.showAnswers(imgRawDrawings, myIndex, grading, ans)  # DRAW ON NEW IMAGE
    #     # invMatrix = cv2.getPerspectiveTransform(pts2, pts1)  # INVERSE TRANSFORMATION MATRIX
    #     # imgInvWarp = cv2.warpPerspective(imgRawDrawings, invMatrix, (widthImg, heightImg))  # INV IMAGE WARP
    #
    #     # blankImg = np.zeros_like(Cimg)
    #     # imageArray = ([CimgBigContour, SimgBigContour, CimgThresh, SimgCanny, ],
    #     #               [blankImg, SimgThresh, blankImg, blankImg, ]
    #     #               )
    #     # stackedImage = utlis.stackImages(imageArray, 0.5)
    #     # cv2.imshow("Result", stackedImage)
    #     # cv2.waitKey(0)
    #     return excel_file
    # elif SRecNum == rect_num and CRecNum != rect_num:
    #     msg = _(
    #         'The Scan Of Correct Answer Paper Is Bad.')
    #     messages.add_message(request, messages.WARNING, msg)
    #
    # elif CRecNum == rect_num and SRecNum != rect_num:
    #     msg = _(
    #         'The Scan Of Student Answer Paper Is Bad.')
    #     messages.add_message(request, messages.WARNING, msg)
    # else:
    #     msg = _(
    #         'Each Paper is have bad scan.')
    #     messages.add_message(request, messages.WARNING, msg)
