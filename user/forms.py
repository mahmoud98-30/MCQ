from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from user.models import Profile


class UserCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=30,
                               help_text='اسم المستخدم يجب ألا يحتوي على مسافات.')
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput(), min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput(), min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError(_('Password does not match'))
        return cd['password2']

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError(_('There is a registered user with this name.'))
        return cd['username']

    def clean_email(self):
        """
           Check the email if exists or not
        """
        cd = self.cleaned_data
        if User.objects.filter(email=cd['email']).exists():
            raise forms.ValidationError(_("The email is already email"))
        return cd['email']


class LoginForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', 'school_name', 'school_address')
