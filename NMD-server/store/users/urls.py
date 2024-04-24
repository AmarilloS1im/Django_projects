from django.contrib.auth.decorators import login_required
from django.urls import path

from users.views import (IndexView, ProfileView, RecoveryView,
                         RegistrationConfirmView, RegistrationView, logout)

app_name = 'users'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('registration_confirm/', RegistrationConfirmView.as_view(), name='registration_confirm'),
    path('recovery/', RecoveryView.as_view(), name='recovery'),
    path('profile/<int:pk>', login_required(ProfileView.as_view()), name='profile'),
    path('logout/', logout, name='logout')
]
