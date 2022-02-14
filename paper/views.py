from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tablib import Dataset
from django.utils.translation import gettext_lazy as _
import matplotlib.pyplot as plt

from paper.correction import chack_answer
from paper.forms import paperForm, StudentForm, TeacherForm, ClassForm, UpdateStudentForm, UpdateTeacherForm, \
    UpdateClassForm
from paper.models import Correct, Student, Teacher, Class
from user.models import Profile
from .filters import StudentFilter
from .generate_pdf import generate_pdf
from .resources import StudentResource


@login_required(login_url='/login/')
def home(request):
    if request.method == 'POST':
        form = paperForm(request.POST, request.FILES or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()

            # get last data
            q = Correct.objects.latest('creat_at')

            # convert image to array
            try:
                c_img_arr = plt.imread(q.correct_image.path)
                s_img_arr = plt.imread(q.answer_image.path)
            except:
                c_img_arr = plt.imread(q.correct_image.path)
                s_img_arr = plt.imread(q.answer_image.path)

            # function of correction
            correction = chack_answer(request, c_img_arr, s_img_arr)

            msg = _(
                'Congratulations, your correction has been successful.')
            messages.add_message(request, messages.SUCCESS, msg)
            return correction
    return render(request, 'paper/index.html', {
        'title': _('home'),
    }, )


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
    student = Student.objects.get(id=4)
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
    student_list = Student.objects.all()
    class_list = Class.objects.all()
    # sessions = Teacher.objects.filter(course__id=c.id)  # First way, forward lookup.
    print(class_list)

    subject_list = Teacher.objects.values_list('subject')
    print(subject_list)

    # student_filter = StudentFilter(request.GET, queryset=student_list)

    if request.method == 'POST':
        school = Profile.objects.get(id=1)
        student = Student.objects.get(id=4)
        generate = generate_pdf(student.qr_code.path, school.image.path, student.name, school.school_name,
                                student.class_room, student.teacher_name.name, student.teacher_name.subject, student.code)
        return generate

    return render(request, 'paper/student/generate_pdf.html', {
        'title': _('generate pdf'),
        'subject_list': subject_list,
        'class_list': class_list,
        'student_filter': student_list,
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
