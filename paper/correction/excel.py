import io
from django.http import HttpResponse
import xlsxwriter

from paper.correction.parameters import questions, CorrectScore, rect_num, widthImg, heightImg, wrong, correct


def ExportExcel(GRADINGLIST, FinelScore, CorrectAns, StudentAns, num_of_students_paper):
    # Create an in-memory output file for the new workbook.
    output = io.BytesIO()

    # creat exile file
    workbook = xlsxwriter.Workbook(output)
    sheet = workbook.add_worksheet()

    # s = [item for sublist in StudentAns for item in sublist]
    # print(s)

    # # data
    print('##################################')
    print("TOTEL CORRECTION", GRADINGLIST)
    print("TOTEL CORRECTION", len(GRADINGLIST))
    print("Finel Score", FinelScore)
    print("Finel Score", len(FinelScore))
    print("Correct Answer", CorrectAns)
    print("Correct Answer", len(CorrectAns))
    print("Student Answer", StudentAns)
    print("Student Answer", len(StudentAns))
    print('##################################')

    # Header
    student_name = "Student Name"
    No_que = "Number Of Question"
    result = "Result"
    stu_answer = "Student Answer"
    corr_ans = "Correct Answer"
    result_percent = "Result By Percent"

    que_num = []
    for num in range(1, 101):
        que_num.append(num)

    Correct = []
    for cor in CorrectAns:
        if cor == 0:
            Correct.append("A")
        elif cor == 1:
            Correct.append("B")
        elif cor == 2:
            Correct.append("C")
        else:
            Correct.append("D")
    # print("CorrectAns", Correct)
    # print("CorrectAns", len(Correct))


    for j in range(1, 7 * num_of_students_paper, 7):
        sheet.write(j + 0, 0, "student name")
        sheet.write(j + 1, 0, "no questions")
        sheet.write(j + 2, 0, "corrct answer")
        sheet.write(j + 3, 0, "student answer")
        sheet.write(j + 4, 0, "corrction")
        sheet.write(j + 5, 0, "result")
        sheet.write(j + 6, 0, "-" * 100)

        for item in range(len(que_num)):
            sheet.write(j + 1, item + 1, str(que_num[item]))
            sheet.write(j + 2, item + 1, Correct[item])

    for stu in StudentAns:
        # print("-------------"*100)
        StudentAnsArr = [item for sublist in stu for item in sublist]
        # print(StudentAnsArr, len(StudentAnsArr))
        Student = []
        for score_unm in StudentAnsArr:
                if score_unm == 0:
                    Student.append("A")
                elif score_unm == 1:
                    Student.append("B")
                elif score_unm == 2:
                    Student.append("C")
                else:
                    Student.append("D")
        print("StudentAns", Student, len(Student))
#       TODO: add counter here
        for item in range(len(que_num)):
            sheet.write(j + 3, item + 1, Student[item])

    #     TotelGRADING = [item for sublist in GRADINGLIST for item in sublist]
    #     # print(TotelGRADING)
    #     GRADING = []
    #     for i in TotelGRADING:
    #         for f in i:
    #             if f == 0:
    #                 GRADING.append(wrong)
    #             else:
    #                 GRADING.append(correct)
    #     AllCorrection = []
    #     for i in range(100, 301, 100):
    #         AllCorrection.append(GRADING[:i])
    #
    #     # print("AllCorrection", AllCorrection, len(AllCorrection))
    #     # print("AllCorrection", AllCorrection[1], len(AllCorrection))
    #     # print("GRADING", GRADING, len(GRADING))
    #     for i in range(0, 3):
    #         print(i)
    #         print(AllCorrection[i])
    #
    #         # for itme in range(0, 100):
    #         #     sheet.write(j + 4, itme + 1, corr[itme])
    #
    #
    #
    # #
    # # TotelGRADING = [item for sublist in GRADINGLIST for item in sublist]
    # # # print(TotelGRADING)
    # # GRADING = []
    # # for i in TotelGRADING:
    # #     for j in i:
    # #         if j == 0:
    # #             GRADING.append(wrong)
    # #         else:
    # #             GRADING.append(correct)
    # # AllCorrection = []
    # # for i in range(100, 301, 100):
    # #     AllCorrection.append(GRADING[:i])
    # # print("AllCorrection", AllCorrection, len(AllCorrection))
    # # print("GRADING", GRADING, len(GRADING))
    # # for f in range(1, 7 * num_of_students_paper, 7):
    # #     for item in range(0, len(GRADING)):
    # #         sheet.write(f + 4, item + 1, GRADING[item])
    #
    # Correction = []
    # # for itemc in AllCorrection:
    # #     print("itemc", itemc, len(itemc))
    # # print("Correction", Correction, len(Correction))
    # # for f in range(1, 7 * num_of_students_paper, 7):
    # #     for item in range(len(que_num)):
    # #         sheet.write(f + 4, item + 1, Correction[item])
    #
    #
    #
    # # write data in file
    # for item in range(len(que_num)):
    #     sheet.write(3, item + 1, Correct[item])
    #     sheet.write(5, item + 1, GRADING[item])
    #
    #     # sheet.write(3, item + 1, Student[item])
    #
    # # sheet.write("A8", PercentScore)
    #
    # Close the workbook before sending the data.
    workbook.close()

    # Rewind the buffer.
    output.seek(0)

    # Set up the Http response.
    filename = 'Result.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response
