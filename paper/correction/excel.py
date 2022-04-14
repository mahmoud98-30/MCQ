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

    # TotelGRADING = [item for sublist in GRADINGLIST for item in sublist]
    # print(TotelGRADING)

    # data
    print('##################################')
    print("TOTEL CORRECTION", GRADINGLIST)
    print("Finel Score", FinelScore)
    print("Correct Answer", CorrectAns)
    print("Student Answer", StudentAns)
    print('##################################')

    # Header
    student_name = "Student Name"
    No_que = "Number Of Question"
    result = "Result"
    stu_answer = "Student Answer"
    corr_ans = "Correct Answer"
    result_percent = "Result By Percent"

    for j in range(1, 7 * num_of_students_paper, 7):
        sheet.write(j + 0, 0, "student name")
        sheet.write(j + 1, 0, "no questions")
        sheet.write(j + 2, 0, "corrct answer")
        sheet.write(j + 3, 0, "student answer")
        sheet.write(j + 4, 0, "corrction")
        sheet.write(j + 5, 0, "result")
        sheet.write(j + 6, 0, "-" * 100)

    que_num = []
    for num in range(1, 101):
        que_num.append(num)

    TotelGRADING = [item for sublist in GRADINGLIST for item in sublist]
    GRADING = []
    for i in TotelGRADING:
        for j in i:
            if i == 0:
                GRADING.append(wrong)
            else:
                GRADING.append(correct)

    # print("GRADING",GRADING,len(GRADING))

    # Correct = []
    # for cor in CorrectAns:
    #     if cor == 0:
    #         Correct.append("A")
    #     elif cor == 1:
    #         Correct.append("B")
    #     elif cor == 2:
    #         Correct.append("C")
    #     else:
    #         Correct.append("D")
    # # print(Correct)
    #
    # Student = []
    # for stu in StudentAns:
    #     if stu == 0:
    #         Student.append("A")
    #     elif stu == 1:
    #         Student.append("B")
    #     elif stu == 2:
    #         Student.append("C")
    #     else:
    #         Student.append("D")
    # # print(Student)
    #
    # # write data in file
    # for item in range(len(que_num)):
    #     sheet.write(1, item + 1, que_num[item])
    #     sheet.write(2, item + 1, GRADING[item])
    #     sheet.write(3, item + 1, Student[item])
    #     sheet.write(4, item + 1, Correct[item])
    #
    # sheet.write("A8", PercentScore)

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

    # return response
