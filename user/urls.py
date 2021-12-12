from django.urls import path, reverse_lazy
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

app_name = 'user'
urlpatterns = [
                  path('register/', views.register, name='register'),
                  path('login/', views.login_user, name='login'),
                  path('logout/', views.logout_user, name='logout'),
                  path('reset_password/',
                       auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
                       name="reset_password"),

                  path('reset_password_sent/',
                       auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html", ),
                       name="password_reset_done"),
                  path(
                      'password/reset/confirm/<uidb64>/<token>/',
                      auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
                      name='password_reset_confirm'
                  ),
                  path('reset_password_complete/',
                       auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
                       name="password_reset_complete"),

                  # path('profile/', views.profile, name='profile'),
                  # path('profile_update/', views.profile_update, name='profile_update'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
