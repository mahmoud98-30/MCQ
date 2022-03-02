import paper.utlis as utlis
from paper.correction.excel import ExportExcel
from paper.correction.parameters import questions, CorrectScore


def finel_correction(CorrectIndex, CorrectAnslist, StudentIndex, StudentAnslist,):

    # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS
    TotelScore = []
    GRADINGLIST = []
    grading = []
    for x in range(0, questions):
        if StudentIndex[x] == CorrectIndex[x]:
            grading.append(1)
        else:
            grading.append(0)

    print("GRADING", grading)
    GRADINGLIST.append(grading)

    score = (sum(grading) / questions) * 100  # FINAL GRADE
    TotelScore.append(score)
    print("SCORE", score)

    # print("TOTEL SCORE", TotelGRADING)
    # print("TOTEL SCORE", TotelScore)

    PercentScore = (sum(TotelScore) / CorrectScore) * 100
    # print("Finel SCORE", PercentScore)

    # put many list from one list ,to one list
    TotelGRADING = [item for sublist in GRADINGLIST for item in sublist]
    CorrectAns = [item for sublist in CorrectAnslist for item in sublist]
    StudentAns = [item for sublist in StudentAnslist for item in sublist]

    # exoprt to excel file
    excel_file = ExportExcel(TotelGRADING, TotelScore, PercentScore, CorrectAns, StudentAns)