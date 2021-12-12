from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from .forms import UserCreationForm, LoginForm, UserUpdateForm


def register(request):
    # form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            messages.success(
                request, f'تهانينا {new_user} لقد تمت عملية التسجيل بنجاح.')
            return redirect('/login/')
    else:
        form = UserCreationForm()
    return render(request, 'user/register.html', {
        'title': 'التسجيل',
        'form': form,
    }, )


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        # email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, 'هناك خطا في اسم المستخدم او كلمة المرور')
    return render(request, 'user/login.html', {
        'title': 'تسجيل الدخول',
    })


def logout_user(request):
    logout(request)
    return redirect('/login/')
