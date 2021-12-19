from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import cv2
from django.conf import settings

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

            messages.success(
                request, 'تهانينا  لقد تمت عملية بنجاح.')
            return redirect('/')

            # cimageURL = settings.MEDIA_URL + form.instance.correct_image.name
            # simageURL = settings.MEDIA_URL + form.instance.answer_image.name
            # print(cimageURL)
            # x = settings.MEDIA_ROOT_URL + cimageURL
            # print(x)

            # opencv_dface(settings.MEDIA_ROOT_URL + imageURL)

            # img = Correct.objects.get(id=4)
            # c_img = str(img.correct_image)
            # s_img = str(img.answer_image)




    else:
        form = paperForm()

    return render(request, 'paper/index.html', {
        'title': 'home',
        'form': form,
    }, )
