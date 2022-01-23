from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tablib import Dataset
from django.utils.translation import gettext_lazy as _
import matplotlib.pyplot as plt

from paper.correction import chack_answer
from paper.forms import paperForm, CreateStudentForm, CreateTeacherForm, CreateClassForm
from paper.models import Correct, Student, Teacher, Class
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
    form = CreateStudentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            msg = _('done ')
            messages.add_message(request, messages.SUCCESS, msg)
        form = CreateStudentForm()
    student = Student.objects.all()
    return render(request, 'paper/student/new_student.html', {
        'title': _('new student'),
        'form': form,
        'student': student,
    })


@login_required(login_url='/login/')
def update_student(request, fk):
    pass


@login_required(login_url='/login/')
def delete_student(request, fk):
    q = Correct.objects.filter(id=fk).delete()
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def delete_all_students(request):
    pass


@login_required(login_url='/login/')
def new_teacher(request):
    form = CreateTeacherForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            msg = _('done ')
            messages.add_message(request, messages.SUCCESS, msg)
        form = CreateTeacherForm()
    teacher = Teacher.objects.all()
    return render(request, 'paper/teacher/new_teacher.html', {
        'title': _('new teacher'),
        'form': form,
        'teacher': teacher,
    })


@login_required(login_url='/login/')
def update_teacher(request):
    pass


@login_required(login_url='/login/')
def delete_teacher(request):
    pass


@login_required(login_url='/login/')
def delete_all_teachers(request):
    pass


@login_required(login_url='/login/')
def new_class(request):
    form = CreateClassForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            msg = _('done ')
            messages.add_message(request, messages.SUCCESS, msg)
        form = CreateClassForm()
    class_room = Class.objects.all()
    return render(request, 'paper/class/new_class.html', {
        'title': _('new class'),
        'form': form,
        'class': class_room,
    })


@login_required(login_url='/login/')
def update_class(request):
    pass


@login_required(login_url='/login/')
def delete_class(request):
    pass


@login_required(login_url='/login/')
def delete_all_class(request):
    pass

