import paper.utlis as utlis
from paper.correction.excel import ExportExcel
from paper.correction.parameters import questions, CorrectScore


def finel_correction(CorrectAnslist, StudentAnslist, ):
    # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS
    CorrectAns = [item for sublist in CorrectAnslist for item in sublist]
    # StudentAns = [item for sublist in StudentAnslist for item in sublist for item2 in item ]
    StudentAns = []
    for sublist in StudentAnslist:
        for item in sublist:
            for item2 in item:
                StudentAns.append(item2)
    print(CorrectAns)
    print(StudentAns)
    # TotelScore = []
    # GRADINGLIST = []
    # grading = []
    # student_paper_num = len(StudentAnslist)
    # for i in range(0, student_paper_num):
    #     # print('c',CorrectAnslist)
    #     s = StudentAnslist[i]
    #     # print('s',StudentAnslist[i])
    #     # print('--------------')
    #     for x in range(0, questions):
    #         # print('c', CorrectAnslist[x])
    #         # print('sx', s[i])
    #         for x in range(0, questions):
    #             print('c', CorrectAnslist[x])
    #             print('sx', s[i])
    #             if s[i] == CorrectAnslist[x]:
    #                 grading.append(1)
    #             else:
    #                 grading.append(0)
    #
    # print("GRADING", grading)
        # GRADINGLIST.append(grading)
        # print(grading[0:10])
        # print(grading[10:20])
        # print(grading[20:30])

    # grading_num = len(grading)
    # for x in range(0, grading_num, 10):
    #     print(grading[x:x + 10])
    #     score = (sum(grading[x:x + 10]) / questions) * 100  # FINAL GRADE
    #     TotelScore.append(score)
    #     print("SCORE", score)

    # # DISPLAYING CORRACT
    # CResultImg = CimgWarpColored.copy()
    # CResultImg = utlis.showAnswers(CResultImg, CorrectIndex, grading, ans)  # DRAW DETECTED ANSWERS
    # utlis.drawGrid(CimgWarpColored)  # DRAW GRID
    #
    # # DISPLAYING ANSWERS
    # SResultImg = SimgWarpColored.copy()
    # SResultImg = utlis.showAnswers(SResultImg, StudentIndex, grading, ans)  # DRAW DETECTED ANSWERS
    # utlis.drawGrid(SimgWarpColored)  # DRAW GRID
    #
    # imgRawDrawings = np.zeros_like(imgWarpColored)  # NEW BLANK IMAGE WITH WARP IMAGE SIZE
    # utlis.showAnswers(imgRawDrawings, myIndex, grading, ans)  # DRAW ON NEW IMAGE
    # invMatrix = cv2.getPerspectiveTransform(pts2, pts1)  # INVERSE TRANSFORMATION MATRIX
    # imgInvWarp = cv2.warpPerspective(imgRawDrawings, invMatrix, (widthImg, heightImg))  # INV IMAGE WARP
    #
    # blankImg = np.zeros_like(Cimg)
    # imageArray = ([CimgBigContour, SimgBigContour, CimgThresh, SimgCanny, ],
    #                   [blankImg, SimgThresh, blankImg, blankImg, ]
    #                   )
    # stackedImage = utlis.stackImages(imageArray, 0.5)
    # cv2.imshow("Result", stackedImage)
    # cv2.waitKey(0)

    # print("TOTEL SCORE", TotelGRADING)
    # print("TOTEL SCORE", TotelScore)

    # PercentScore = (sum(TotelScore) / CorrectScore) * 100
    # # print("Finel SCORE", PercentScore)
    #
    # # put many list from one list ,to one list
    # TotelGRADING = [item for sublist in GRADINGLIST for item in sublist]
    # CorrectAns = [item for sublist in CorrectAnslist for item in sublist]
    # StudentAns = [item for sublist in StudentAnslist for item in sublist]
    #
    # # exoprt to excel file
    # excel_file = ExportExcel(TotelGRADING, TotelScore, PercentScore, CorrectAns, StudentAns)
    # return excel_file
