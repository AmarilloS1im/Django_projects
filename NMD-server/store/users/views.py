from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, FormView, TemplateView, UpdateView
from django.apps.registry import apps


from .models import User
from  .forms import UserLoginForm, UserProfileForm, UserRegistrationForm



def index(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(email=email, password=password)
            if user:
                auth.login(request,user)
                return HttpResponseRedirect(reverse('products:products'))
        else:
            print(form.cleaned_data)
            print(form.errors)
            print(form.non_field_errors())
            print(form.errors.as_data())
    else:
        form = UserLoginForm()
    context = {
        'title': "Вход/Регирстрация",
        'header': "Сайт предзаказа для сотрудников",
        'form_label': "Авторизация",
        'form': form,
    }

    return render(request,'users/index.html',context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            created_user = User.objects.last()
            password = User.objects.make_random_password(length=15)
            created_user.set_password(password)
            created_user.save(update_fields=['password'])
            created_user.username = created_user.email
            created_user.save()
            print(password)
            send_mail('Ваш Пароль от сайта Никамед предзаказ', f'ВАШ ПАРОЛЬ: {password}', settings.EMAIL_HOST_USER, [f'{created_user.email}'])
            return HttpResponseRedirect(reverse('users:registration_confirm'))
        else:
            context = {
                'title': "Регирстрация",
                'header': "Регистрация",
                'form_label': "Регистрация",
                'form': form
            }
            print(form.errors)
            return render(request, 'users/registration.html', context)
    form = UserRegistrationForm()
    context = {
        'title': "Регирстрация",
        'header': "Регистрация",
        'form_label': "Регистрация",
        'form': form,
    }
    return render(request, 'users/registration.html', context)

def registration_confirm(request):
    context = {
        'title': "Подтверждение регистрации",
        'header': "Подтверждение регистрации",
        'form_label': "Вы успешно зарегистрированы. Пароль отправлен на вашу почту. Введите почту и пароль на главной странице для входа на сайт.",
    }
    return render(request, 'users/registration_confirm.html', context)


def recovery(request):
    context = {
        'title': "Восстановление данных",
        'header': "Восстановление данных",
        'form_label': "Восстановить пароль",
    }
    return render(request, 'users/recovery.html', context)

def profile(request,pk):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'title': "Личный кабинет",
        'form': form,
    }
    return render(request, 'users/profile.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:index'))
