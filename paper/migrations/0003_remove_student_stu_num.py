# Generated by Django 2.2.13 on 2022-01-18 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0002_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='stu_num',
        ),
    ]