from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import cv2
from django.utils.translation import gettext_lazy as _
import matplotlib.pyplot as plt
from paper.correction import chack_answer
from paper.forms import paperForm
from paper.models import Correct


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
def delete_all_papers(request):
    # delete all data
    q = Correct.objects.all().delete()
    return HttpResponseRedirect("/")
