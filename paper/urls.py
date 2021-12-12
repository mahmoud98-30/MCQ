from django.urls import path
from . import views

app_name = 'paper'
urlpatterns = [
    path('', views.home, name='home'),

]
