from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def home(request):
    context = {
        'title': 'الصفحة الرئيسية',

    }
    return render(request, 'paper/index.html', context)
