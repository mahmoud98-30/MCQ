from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pyexpat.errors import messages

from paper.correction import chack_answer
from paper.forms import paperForm
from paper.models import Correct


@login_required(login_url='/login/')
def home(request):
    if request.method == 'POST':
        form = paperForm(request.POST, request.FILES)
        if form.is_valid():
            save = form.save(commit=False)
            title = form.cleaned_data['title']
            cimg = str(form.cleaned_data['correct_image'])
            simg = str(form.cleaned_data['answer_image'])
            form.save()
            img = Correct.objects.get(id=4)
            c_img = str(img.correct_image)
            s_img = str(img.answer_image)

            # chack_answer(c_img, s_img)
            # print("sand is done")
            form = paperForm()

    else:
        form = paperForm()

    return render(request, 'paper/index.html', {
        'title': 'home',
        'form': form,
    }, )
