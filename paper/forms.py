from django import forms
from django.utils.translation import ugettext_lazy as _

from paper.models import Correct, Student


class paperForm(forms.ModelForm):
    title = forms.CharField()
    correct_image = forms.ImageField()
    answer_image = forms.ImageField()

    class Meta:
        labels = {'title': _('title'), 'correct_image': _('correct_image'),
                  'answer_image': _('answer_image'), }
        model = Correct
        fields = ('title', 'correct_image', 'answer_image')


class UploadStudentForm(forms.ModelForm):

    class Meta:
        labels = {'name': _('name'),
                  'teacher_name': _('teacher_name'), 'subject': _('subject'), }
        model = Student
        fields = ('name', 'teacher_name', 'subject')
