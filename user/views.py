from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.utils.translation import gettext_lazy as _
from django.utils.translation.trans_null import ngettext_lazy

from .forms import UserCreationForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


@login_required(login_url='/login/')
def register(request):
    # form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            username = form.cleaned_data.get('username')
            new_user.save()
            msg = _(
                f'Congratulations {username} Your registration has been completed successfully.')
            messages.add_message(request, messages.SUCCESS, msg)
            return redirect('/login/')
    else:
        form = UserCreationForm()
    return render(request, 'user/register.html', {
        'title': _('register'),
        'form': form,
    }, )


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            msg = _('There is an error in the username or password')
            messages.add_message(request, messages.WARNING, msg)
    return render(request, 'user/login.html', {
        'title': _('Login'),
    })


def logout_user(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def profile(request):
    profile_data = Profile.objects.filter(user=request.user)
    return render(request, 'user/profile.html', {
        'title': _('profile'),
        'profile_data': profile_data,

    })


@login_required(login_url='/login/')
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()

            msg = _('Modified successfully.')
            messages.add_message(request, messages.SUCCESS, msg)

            return redirect('/profile/')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': _('profile update'),
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user/profile_update.html', context)
