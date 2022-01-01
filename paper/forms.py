from django import forms
from django.utils.translation import ugettext_lazy as _

from paper.models import Correct


class paperForm(forms.ModelForm):
    title = forms.CharField(label='اسم المادة')
    correct_image = forms.ImageField(label='ورقة النموذج الصحيحه')
    answer_image = forms.ImageField(label='ورقة الطالب')

    class Meta:
        labels = {'title': _('title'), 'correct_image': _('correct_image'),
                  'answer_image': _('answer_image'), }
        model = Correct
        fields = ('title', 'correct_image', 'answer_image')
