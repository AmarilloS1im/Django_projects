from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path
from .views import *



app_name = 'users'
urlpatterns = [
    path('', index, name='index'),
    path('registration/', registration, name='registration'),
    path('registration_confirm/', registration_confirm, name='registration_confirm'),
    path('recovery/', recovery, name='recovery'),
    path('profile/<int:pk>',profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('password-change/', UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"), name="password_change_done"),

]
