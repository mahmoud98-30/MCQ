from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from paper.models import Correct, Student


@admin.register(Student)
class PersonAdmin(ImportExportModelAdmin):
    list_display = ('name', "id", 'teacher_name', 'subject', 'qr_code')


admin.site.register(Correct)
# admin.site.register(Student)
