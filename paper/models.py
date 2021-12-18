from django.db import models
from django.utils.translation import gettext_lazy as _
import cv2

from paper.correction import chack_answer


class Correct(models.Model):
    title = models.CharField(max_length=225)
    correct_image = models.ImageField(blank=True, upload_to='correct-paper/', default='correct.png')
    answer_image = models.ImageField(blank=True, upload_to='answer-paper/', default='correct.png')
    creat_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Correct')
        verbose_name_plural = _('Corrects')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        c_img_arr = cv2.imread(self.correct_image.path)
        s_img_arr = cv2.imread(self.answer_image.path)
        chack_answer(c_img_arr, s_img_arr)
