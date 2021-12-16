from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pyexpat.errors import messages

from paper.forms import paperForm


@login_required(login_url='/login/')
def home(request):
    if request.method == 'POST':
        form = paperForm(request.POST)
        print(form)
        if form.is_valid():
            # img = form.save(commit=False)
            title = form.cleaned_data['title']
            img = form.cleaned_data['correct_image']
            img2 = form.cleaned_data['answer_image']
            print(title)
            print(img)
            print(type(img))

    else:
        form = paperForm()

    return render(request, 'paper/index.html', {
        'title': 'home',
        'form': form,
    }, )


