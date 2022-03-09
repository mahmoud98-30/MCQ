import paper.utlis as utlis
from paper.correction.excel import ExportExcel
from paper.correction.parameters import questions, CorrectScore


def finel_correction(CorrectAnslist, StudentAnslist, ):
    # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS
    TotelScore = []
    GRADINGLIST = []
    grading = []
    student_paper_num = len(StudentAnslist)
    for i in range(0, student_paper_num):
        # print('c',CorrectAnslist)
        s = StudentAnslist[i]
        # print('s',StudentAnslist[i])
        # print('--------------')
        for x in range(0, questions):
            # print('c', CorrectAnslist[x])
            # print('sx', s[x])
            if s[x] == CorrectAnslist[x]:
                grading.append(1)
            else:
                grading.append(0)

    print("GRADING", grading)
        # GRADINGLIST.append(grading)
        # print(grading[0:10])
        # print(grading[10:20])
        # print(grading[20:30])

    grading_num = len(grading)
    for x in range(0, grading_num, 10):
        print(grading[x:x + 10])
        score = (sum(grading[x:x + 10]) / questions) * 100  # FINAL GRADE
        TotelScore.append(score)
        print("SCORE", score)

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
