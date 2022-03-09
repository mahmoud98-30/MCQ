from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'paper'
urlpatterns = [
                  path('', views.home, name='home'),
                  path('paper-list/', views.paper_list, name='paper-list'),
                  path('import-student-data/', views.import_student_data, name='import-student-data'),
                  path('delete-papers/', views.delete_all_papers, name='delete-papers'),
                  path('new-student/', views.new_student, name='new-student'),
                  path('generate-pdf/', views.generate_pdf, name='generate-pdf'),


                  path('update-student/<int:fk>/', views.update_student, name='update-student'),
                  path('delete-student/<int:fk>/', views.delete_student, name='delete-student'),
                  path('delete-all-students/', views.delete_all_students, name='delete-all-students'),

                  path('new-teacher/', views.new_teacher, name='new-teacher'),
                  path('update-teacher/<int:fk>/', views.update_teacher, name='update-teacher'),
                  path('delete-teacher/<int:fk>/', views.delete_teacher, name='delete-teacher'),
                  path('delete-all-teachers/', views.delete_all_teachers, name='delete-all-teachers'),

                  path('new-class/', views.new_class, name='new-class'),
                  path('update-class/<int:fk>/', views.update_class, name='update-class'),
                  path('delete-class/<int:fk>/', views.delete_class, name='delete-class'),
                  path('delete-all-class/', views.delete_all_class, name='delete-all-class'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
