from django.db import models
from django.utils.translation import gettext_lazy as _
import qrcode


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


class Student(models.Model):
    name = models.CharField(max_length=225)
    teacher_name = models.CharField(max_length=225)
    subject = models.CharField(max_length=225)
    qr_code = models.ImageField(blank=True, upload_to='QR-code/', default='qrcode.png')

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Student')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        data = self.id, self.name, self.teacher_name, self.subject
        img = qrcode.make(data)
        img.save("qr.png")
        super().save(*args, **kwargs)
