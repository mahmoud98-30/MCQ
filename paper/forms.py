from django import forms
from django.utils.translation import ugettext_lazy as _

from paper.models import Correct, Student, Teacher, Class


class paperForm(forms.ModelForm):
    title = forms.CharField()
    correct_image = forms.ImageField()
    answer_image = forms.ImageField()

    class Meta:
        labels = {'title': _('title'), 'correct_image': _('correct_image'),
                  'answer_image': _('answer_image'), }
        model = Correct
        fields = ('title', 'correct_image', 'answer_image')


class StudentForm(forms.ModelForm):
    class Meta:
        labels = {'name': _('name'), 'code': _('code'),
                  'class_room': _('class_room'), 'teacher_name': _('teacher_name'), }
        model = Student
        fields = ('name', 'code', 'class_room', 'teacher_name')

    def clean_code(self):
        """
           Check the email if exists or not
        """
        cd = self.cleaned_data
        if Student.objects.filter(code=cd['code']).exists():
            raise forms.ValidationError(_("The code is already "))
        return cd['code']


class UpdateStudentForm(forms.ModelForm):
    class Meta:
        labels = {'name': _('name'), 'code': _('code'),
                  'class_room': _('class_room'), 'teacher_name': _('teacher_name'), }
        model = Student
        fields = ('name', 'code', 'class_room', 'teacher_name')


class TeacherForm(forms.ModelForm):
    class Meta:
        labels = {'name': _('name'), 'subject': _('subject'),
                  }
        model = Teacher
        fields = ('name', 'subject',)


class UpdateTeacherForm(forms.ModelForm):
    class Meta:
        labels = {'name': _('name'), 'subject': _('subject'),
                  }
        model = Teacher
        fields = ('name', 'subject',)


class ClassForm(forms.ModelForm):
    class Meta:
        labels = {'name': _('name'),
                  }
        model = Class
        fields = ('name',)


class UpdateClassForm(forms.ModelForm):
    class Meta:
        labels = {'name': _('name'),
                  }
        model = Class
        fields = ('name',)
