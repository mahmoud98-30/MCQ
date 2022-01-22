from random import random, randrange, getrandbits, randint
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File


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


class Class(models.Model):
    name = models.CharField(max_length=225)

    class Meta:
        verbose_name = _('Class')
        verbose_name_plural = _('Class')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Teacher(models.Model):
    SUBJECT = (
        ('Math', _('Math')),
        ('Sciences', _('Sciences')),
        ('Grammar', _('Grammar')),
        ('Biology', _('Biology')),
        ('Chemistry', _('Chemistry')),
        ('Geography', _('Geography')),
        ('Einglish', _('Einglish')),
        ('History', _('History')),
        ('Computer', _('Computer')),
        ('Physics', _('Physics')),
        ('Islam', _('Islam')),
        ('National Education', _('National Education')),
        ('Statistics', _('Statistics')),
        ('philosophy', _('philosophy')),
        ('psychology', _('psychology')),
        ('Reading', _('Reading')),
        ('Literary Studies', _('Literary Studies')),

    )
    name = models.CharField(max_length=225)
    subject = models.CharField(max_length=100, choices=SUBJECT)

    class Meta:
        verbose_name = _('Teacher')
        verbose_name_plural = _('Teacher')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Student(models.Model):
    name = models.CharField(max_length=225)
    code = models.CharField(max_length=225)
    class_room = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True, )
    teacher_name = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True, )
    qr_code = models.ImageField(blank=True, upload_to='QR-code/', default='qrcode.png')

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Student')

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="{}" height="100"/>'.format(self.qr_code.url))

    image_tag.short_description = 'Image'
    image_tag.allow_tages = True

    def save(self, *args, **kwargs):
        data = self.code, self.name, self.class_room.name, self.teacher_name.name, self.teacher_name.subject
        img = qrcode.make(data)
        buffer = BytesIO()
        img.save(buffer)
        self.qr_code.save(f'QR code{self.name,}, {randint(0, 9999)}.png', File(buffer), save=False)
        img.close()
        super().save(*args, **kwargs)

