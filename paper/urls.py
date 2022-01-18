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

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
