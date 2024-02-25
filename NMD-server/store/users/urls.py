
from django.urls import path
from users.views import index, registration, registration_confirm, recovery, profile,logout

app_name = 'users'
urlpatterns = [
    path('', index, name='index'),
    path('registration/', registration, name='registration'),
    path('registration_confirm/', registration_confirm, name='registration_confirm'),
    path('recovery/', recovery, name='recovery'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout')
]

