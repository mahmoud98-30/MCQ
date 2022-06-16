from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404

from fpdf import FPDF
import io
import time
from django.http import FileResponse, HttpResponseRedirect


def generate(student_data, school):

    school = school.school_name
    # school_logo = school.image.path
    # print(school_logo)



    # Create an in-memory output file for the new workbook.
    output = io.BytesIO()

    # create FPDF object
    pdf = FPDF('p', 'mm', 'A4')

    for student in student_data:
        print(student, student.qr_code.path, student.class_room.name, student.teacher_name.name, student.teacher_name.subject, student.code)

        # Add a page
        pdf.add_page()

        # specify font
        pdf.add_font('DejaVu', '', 'paper\DejaVuSans.ttf', uni=True)
        pdf.set_font('DejaVu', '', 16)
        pdf.set_text_color(0, 0, 0)

        # Add text
        # Move to the right
        pdf.cell(80)

        # write school name as header

        pdf.cell(30, 10, school, 0, 0, 'C')

        # Line break
        pdf.ln(20)

        # add RQ code for student
        pdf.image(student.qr_code.path, x=10, y=8, w=30)

        # pdf.image(school_logo, x=160, y=8, w=30)

        # Line break
        pdf.ln(20)

        pdf.set_font('DejaVu', '', 13)

        # write class room
        class_room_name = u'class :' + str(student.class_room.name)
        pdf.cell(130, 10, class_room_name, )

        # write student name
        student_name = u'name :' + str(student)
        pdf.cell(80, 10, student_name, )

        # Line break
        pdf.ln(10)

        # write teacher name
        teacher_name = u'teacher :' + student.teacher_name.name
        pdf.cell(130, 10, teacher_name, )

        # write student code
        code = u'student code :' + student.code
        pdf.cell(80, 10, code, )

        # Line break
        pdf.ln(60)

        # draw the right rectangle
        pdf.cell(10, )
        pdf.cell(5, -70, "correct", )
        pdf.rect(19, 90, 21, 5, style='D')

        # draw circle in right rectangle
        pdf.ellipse(20, 91, 3, 3, style='D')
        pdf.ellipse(25, 91, 3, 3, style='F')
        pdf.ellipse(30, 91, 3, 3, style='D')
        pdf.ellipse(35, 91, 3, 3, style='D')

        # draw the lift rectangle
        pdf.cell(130, )
        pdf.cell(70, -70, "wrong", )
        pdf.rect(152, 89, 21, 5, style='D')

        # draw circle in lift rectangle
        pdf.set_draw_color(r=0, g=0, b=0)
        pdf.line(x1=153, y1=90, x2=156, y2=93)
        pdf.line(x1=153, y1=93, x2=156, y2=90)
        pdf.ellipse(153, 90, 3, 3, style='D')

        pdf.set_draw_color(r=0, g=0, b=0)
        pdf.line(x1=158, y1=90, x2=159, y2=92)
        pdf.line(x1=159, y1=92, x2=163, y2=89)
        pdf.ellipse(158, 90, 3, 3, style='D')

        pdf.ellipse(163, 90, 3, 3, style='D')
        pdf.ellipse(163.5, 90.7, 1.8, 1.8, style='F')

        pdf.ellipse(168, 90, 3, 3, style='D')

        # Line break
        pdf.ln(30)  # 50

        pdf.set_line_width(0.4)
        pdf.set_font('DejaVu', '', 11)


        #
        # x = 10
        # y = str(x)
        #
        # # top
        # pdf.cell(-2, )
        # pdf.cell(2, -53, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -41, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -29, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -17, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -5, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 7, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 19, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 32, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 44, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 56, y, )
        #
        # # -----------------------------
        #
        # pdf.cell(38, )
        # pdf.cell(2, -53, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -41, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -29, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -17, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -5, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 7, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 19, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 32, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 44, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 56, y, )
        #
        # # -----------------------------
        #
        # pdf.cell(38, )
        # pdf.cell(2, -53, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -41, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -29, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -17, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -5, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 7, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 19, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 32, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 44, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 56, y, )
        #
        # # -----------------------------
        # pdf.cell(38, )
        # pdf.cell(2, -53, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -41, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -29, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -17, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -5, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 7, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 19, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 32, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 44, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 56, y, )
        #
        # # -----------------------------
        #
        # pdf.cell(38, )
        # pdf.cell(2, -53, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -41, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -29, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -17, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, -5, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 7, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 19, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 32, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 44, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 56, y, )
        #
        # # ########### bottom ##############
        # pdf.cell(-162, )
        # pdf.cell(2, 88, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 100, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 112, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 124, y, )

        # pdf.ln(-7)
        # pdf.cell(-2, )
        # pdf.cell(2, 136, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 148, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 160, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 172, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 184, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 196, y, )
        #

        # -----------------------------
        # pdf.cell(38, )
        # pdf.cell(2, 88, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 100, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 112, y, )

        # pdf.cell(-2, )
        # pdf.cell(2, 124, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 136, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 148, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 160, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 172, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 184, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 196, y, )

        # # -----------------------------
        #
        # pdf.cell(38, )
        # pdf.cell(2, 88, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 100, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 112, y, )
        #
        # # pdf.cell(-2, )
        # pdf.cell(2, 124, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 136, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 148, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 160, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 172, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 184, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 196, y, )

        # # -----------------------------

        # pdf.cell(38, )
        # pdf.cell(2, 88, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 100, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 112, y, )

        # pdf.cell(-2, )
        # pdf.cell(2, 124, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 136, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 148, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 160, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 172, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 184, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 196, y, )

        # # -----------------------------
        # pdf.cell(38, )
        # pdf.cell(2, 88, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 100, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 112, y, )
        # #

        # pdf.cell(-2, )
        # pdf.cell(2, 124, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 136, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 148, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 160, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 172, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 184, y, )
        #
        # pdf.cell(-2, )
        # pdf.cell(2, 196, y, )

        for j in range(1, 140, 70):  # 2 rectangle row
            # print(j)
            for i in range(1, 200, 40):  # 5 rectangle in 1 row
                # print(i)
                pdf.cell(1, -65, "A  B  C  D", )
                pdf.cell(33, 75, "A  B  C  D", )
                pdf.rect(14 + i, 129 + j, 23.2, 60, style='D')
                for k in range(1, 60, 6):  # 10 ellipse row
                    # print(k)
                    for t in range(1, 20, 5):  # 4 ellipse in 1 row
                        # print(t)
                        pdf.ellipse(15.5 + t + i, 130 + k + j, 3, 3, style='D')

        # pdf.output('test.pdf')
        # Rewind the buffer.
        date = time.strftime("%Y-%m-%d")
    name = "report.pdf"
    suffix = datetime.now().strftime("%y%m%d_%H%M%S")
    print(suffix)
    # filename = teacher + " " + suject + " " + " " + name
    filename = "_".join([student.teacher_name.name, suffix, name,])
    pdf.output(filename, 'F')
    output.seek(0)

    return FileResponse(open(filename, 'rb'), as_attachment=True, content_type='application/pdf')


def gen(request):

    return render(request, 'paper/student/update_student.html', {
        'title': _('update student'),

    })