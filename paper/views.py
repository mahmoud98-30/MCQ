from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tablib import Dataset
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView

from paper.correction import chack_answer
from paper.forms import CorrectForm, CorrectionForm, StudentForm, TeacherForm, ClassForm, UpdateStudentForm, UpdateTeacherForm, \
    UpdateClassForm
from paper.models import Correct, Student, Teacher, Class, Correction
from user.models import Profile
from .filters import StudentFilter
from .generate_pdf import generate
from .resources import StudentResource


@login_required(login_url='/login/')
def home(request):
    correct_form = CorrectForm(request.POST, request.FILES or None)
    correction_form = CorrectionForm(request.POST, request.FILES or None)
    if request.method == 'POST':
        if correct_form.is_valid and correction_form.is_valid:

            correct_form = correct_form.save(commit=False)
            correct_form.save()

            title = request.POST.get('title')
            images = request.FILES.getlist('answer_image')
            for img in images:
                value = Correction(
                    title=title,
                    answer_image=img,
                    correct_image_id=correct_form.id,
                )
                value.save()

            # get last data
            correct_paper = Correct.objects.latest('creat_at')
            answer_img = Correction.objects.filter(correct_image_id=correct_form.id)

            correct_img = correct_paper.correct_image.path

            # function of correction
            correction = chack_answer(request, correct_img, answer_img)

            msg = _(
                'Congratulations, your correction has been successful.')
            messages.add_message(request, messages.SUCCESS, msg)
            return correction
    return render(request, 'paper/index.html', {
        'title': _('home'),
        'correct_form': correct_form,
        'correction_form': correction_form,
    }, )

# @login_required(login_url='/login/')
# class HomeView(FormView):
#     form_class = CorrectionForm, CorrectForm
#     template_name = 'paper/index.html'  # Replace with your template.
#     success_url = '/'  # Replace with your URL or reverse().
#
#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         files = request.FILES.getlist('answer_image')
#         if form.is_valid():
#             for f in files:
#                 print(f)
#                 # value = Student()
#
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#

@login_required(login_url='/login/')
def paper_list(request):
    # get data
    q = Correct.objects.all()
    return render(request, 'paper/paper.html', {
        'title': _('papers'),
        'q': q,

    }, )


@login_required(login_url='/login/')
def import_student_data(request):
    if request.method == 'POST':
        person_resource = StudentResource()
        dataset = Dataset()
        new_persons = request.FILES['uploadfile']

        imported_data = dataset.load(new_persons.read(), format='xlsx')
        for data in imported_data:
            value = Student(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],

            )
            value.save()

            # result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        # if not result.has_errors():
        #    person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'paper/import_student.html')


@login_required(login_url='/login/')
def delete_all_papers(request):
    # delete all data
    q = Correct.objects.all().delete()
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def new_student(request):
    form = StudentForm(request.POST or None)
    student = Student.objects.all()
    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            msg = _('done ')
            messages.add_message(request, messages.SUCCESS, msg)
        form = StudentForm()

    return render(request, 'paper/student/new_student.html', {
        'title': _('new student'),
        'form': form,
        'student': student,
    })


@login_required(login_url='/login/')
def generate_pdf(request):
    student_filter = Student.objects.all()
    class_list = Class.objects.all()
    # print(request.user.id)
    school_profil = Profile.objects.get(user_id=request.user.id)
    # print(class_list)

    subject_list = Teacher.objects.values_list('subject', flat=True)
    # print(subject_list)
    global class_q
    global subject_q

    class_q = request.POST.get('class_room')
    subject_q = request.POST.get('subject')

    if request.method == 'POST' and "filter" in request.POST:
        # print(request.POST)
        # print(type(class_q), type(subject_q))
        if class_q == subject_q == "ALL":
            student_filter = Student.objects.all()
            # print(student_filter)
        else:
            student_filter = Student.objects.filter(class_room__name=class_q, teacher_name__subject=subject_q)

        return render(request, 'paper/student/generate_pdf.html', {
            'title': _('generate pdf'),
            'subject_list': subject_list,
            'class_list': class_list,
            'student_filter': student_filter,
            'class_q': class_q,
            'subject_q': subject_q,
        })
    if request.method == 'POST' and "tales" in request.POST:
        class_t = request.POST.get('class_t')
        subject_t = request.POST.get('subject_t')
        if class_t is None or subject_t is None:
            msg = _('Enter value in select fields ')
            messages.add_message(request, messages.ERROR, msg)
        else:
            student_filter = Student.objects.filter(class_room__name=class_t, teacher_name__subject=subject_t)
            # print(student_filter)
            generate_paper = generate(student_filter, school_profil,)

            # for student_data in student_filter:
            #
            #     generate_paper = generate(student_data.qr_code.path, school_profil.image.path, student_filter,
            #     school_profil.school_name, student_data.class_room.name, student_data.teacher_name.name,
            #     student_data.teacher_name.subject, student_data.code)

        return generate_paper

    return render(request, 'paper/student/generate_pdf.html', {
        'title': _('generate pdf'),
        'subject_list': subject_list,
        'class_list': class_list,
        'student_filter': student_filter,
        'class_q': class_q,
        'subject_q': subject_q,
    })


@login_required(login_url='/login/')
def update_student(request, fk):
    obj = get_object_or_404(Student, id=fk)
    form = UpdateStudentForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/new-student/")

    return render(request, 'paper/student/update_student.html', {
        'title': _('update student'),
        'form': form,
    })


@login_required(login_url='/login/')
def delete_student(request, fk):
    Student.objects.filter(id=fk).delete()
    return HttpResponseRedirect("/new-student/")


@login_required(login_url='/login/')
def delete_all_students(request):
    Student.objects.all()
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def new_teacher(request):
    form = TeacherForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            msg = _('done ')
            messages.add_message(request, messages.SUCCESS, msg)
        form = TeacherForm()
    teacher = Teacher.objects.all()
    return render(request, 'paper/teacher/new_teacher.html', {
        'title': _('new teacher'),
        'form': form,
        'teacher': teacher,
    })


@login_required(login_url='/login/')
def update_teacher(request, fk):
    obj = get_object_or_404(Student, id=fk)
    form = UpdateTeacherForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/new-teacher/")

    return render(request, 'paper/teacher/update_teacher.html', {
        'title': _('update teacher'),
        'form': form,
    })


@login_required(login_url='/login/')
def delete_teacher(request, fk):
    Teacher.objects.filter(id=fk).delete()
    return HttpResponseRedirect("/new-teacher/")


@login_required(login_url='/login/')
def delete_all_teachers(request):
    Teacher.objects.all()
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def new_class(request):
    form = ClassForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            msg = _('done ')
            messages.add_message(request, messages.SUCCESS, msg)
        form = ClassForm()
    class_room = Class.objects.all()
    return render(request, 'paper/class/new_class.html', {
        'title': _('new class'),
        'form': form,
        'class': class_room,
    })


@login_required(login_url='/login/')
def update_class(request, fk):
    obj = get_object_or_404(Student, id=fk)
    form = UpdateClassForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/new-class/")

    return render(request, 'paper/class/update_class.html', {
        'title': _('update class'),
        'form': form,
    })


@login_required(login_url='/login/')
def delete_class(request, fk):
    Class.objects.filter(id=fk).delete()
    return HttpResponseRedirect("/new-class/")


@login_required(login_url='/login/')
def delete_all_class(request):
    Class.objects.all()
    return HttpResponseRedirect("/")
