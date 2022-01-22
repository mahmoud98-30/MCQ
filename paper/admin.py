from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from paper.models import Correct, Student, Teacher, Class


# @admin.register(Student)
# class PersonAdmin(ImportExportModelAdmin):
#     list_display = ('name', "code", "class_room", 'teacher_name', 'qr_code')
#     fields = ('image_tag',)
#     readonly_fields = ('image_tag',)
#

admin.site.register(Correct)
admin.site.register(Teacher)
admin.site.register(Class)
admin.site.register(Student)
