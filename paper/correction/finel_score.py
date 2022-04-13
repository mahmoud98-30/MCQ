import cv2
import numpy as np

import paper.utlis as utlis
from paper.correction.excel import ExportExcel
from paper.correction.parameters import questions, CorrectScore, rect_num, widthImg, heightImg


def finel_correction(CorrectAnslist, StudentAnslist, SimgWarpColored, Simg, pts1, pts2):
    # print("CorrectAnslist", CorrectAnslist)
    # print("StudentAnslist", StudentAnslist)
    # print("NUM StudentAnslist", len(StudentAnslist))
    # print("-" * 100)
    num_of_students_paper = len(StudentAnslist)

    # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS
    TotelScore = []
    FinelScore = []
    for i in range(0, num_of_students_paper):
        c1 = CorrectAnslist
        s1 = StudentAnslist[i]
        # print("CorrectAnslist", c1)
        # print("StudentAnslist", s1)
        # print("-"*100)
        print("-" * 100)
        for j in range(0, rect_num):
            c2 = c1[j]
            s2 = s1[j]
            # print("c", c2)
            # print("s", s2)
            # print("-" * 100)
            grading = []
            for k in range(0, questions):
                if s2[k] == c2[k]:
                    grading.append(1)
                else:
                    grading.append(0)
                # print("c", c2[k], "s", s2[k])
                # print("-" * 100)

            # utlis.showAnswers(SimgWarpColored, c1[j], grading,
            #                  s1[j])  # DRAW DETECTED ANSWERS
            imgRawDrawings = np.zeros_like(SimgWarpColored)  # NEW BLANK IMAGE WITH WARP IMAGE SIZE
            imgRawDrawings = utlis.showAnswers(imgRawDrawings, c1[j], grading, s1[j])  # DRAW ON NEW IMAGE
            invMatrix = cv2.getPerspectiveTransform(pts2, pts1)  # INVERSE TRANSFORMATION MATRIX
            print(pts2, pts1)
            imgInvWarp = cv2.warpPerspective(imgRawDrawings, invMatrix, (widthImg, heightImg))  # INV IMAGE WARP
            imgFinal = Simg.copy()
            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarp, 1, 0)
            # utlis.drawGrid(SimgWarpColored)  # DRAW GRID

            img = cv2.resize(imgFinal, (800, 800))  # RESIZE IMAGE
            cv2.imshow("SimgWarpColored", img)
            cv2.waitKey(0)

            # print("c1[j] ", c1[j])
            # print("s1[j] ", s1[j])
            # print("GRADING ", grading)
            score = (sum(grading) / questions) * 100  # FINAL GRADE
            TotelScore.append(score)
            # print("SCORE", score)

        PercentScore = (sum(TotelScore) / CorrectScore) * 100
        FinelScore.append(PercentScore)

        # TODO : FinelScore[i] include all final scores in one list

        # print("Finel SCORE", FinelScore[0], "%")



    # DISPLAYING CORRACT
    #ResultImg = CimgWarpColored.copy()
    # ResultImg = utlis.showAnswers(SimgWarpColored, CorrectIndex, grading, StudentIndex)  # DRAW DETECTED ANSWERS
    # utlis.drawGrid(SimgWarpColored)  # DRAW GRID
    # imgRawDrawings = np.zeros_like(imgWarpColored)  # NEW BLANK IMAGE WITH WARP IMAGE SIZE
    # utlis.showAnswers(imgRawDrawings, myIndex, grading, ans)  # DRAW ON NEW IMAGE
    # invMatrix = cv2.getPerspectiveTransform(pts2, pts1)  # INVERSE TRANSFORMATION MATRIX
    # imgInvWarp = cv2.warpPerspective(imgRawDrawings, invMatrix, (widthImg, heightImg))  # INV IMAGE WARP

    # blankImg = np.zeros_like(Cimg)
    # imageArray = ([CimgBigContour, SimgBigContour, CimgThresh, SimgCanny, ])
    # stackedImage = utlis.stackImages(imageArray, 0.5)
    # cv2.imshow("Result", stackedImage)
    # cv2.waitKey(0)



    # # put many list from one list ,to one list
    # TotelGRADING = [item for sublist in GRADINGLIST for item in sublist]
    # CorrectAns = [item for sublist in CorrectAnslist for item in sublist]
    # StudentAns = [item for sublist in StudentAnslist for item in sublist]
    #
    # # exoprt to excel file
    # excel_file = ExportExcel(TotelGRADING, TotelScore, PercentScore, CorrectAns, StudentAns)
    # return excel_file
