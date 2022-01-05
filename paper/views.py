from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import cv2
from django.utils.translation import gettext_lazy as _

from paper.correction import chack_answer
from paper.forms import paperForm
from paper.models import Correct


@login_required(login_url='/login/')
def home(request):
    if request.method == 'POST':
        form = paperForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()

            # get last data
            q = Correct.objects.latest('creat_at')

            # convert image to array
            c_img_arr = cv2.imread(q.correct_image.path)
            s_img_arr = cv2.imread(q.answer_image.path)

            # function of correction
            correction = chack_answer(c_img_arr, s_img_arr)

            msg = _(
                'Congratulations, your correction has been successful.')
            messages.add_message(request, messages.SUCCESS, msg)
            return correction
    else:
        form = paperForm()

    return render(request, 'paper/index.html', {
        'title': _('home'),
        'form': form,
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
