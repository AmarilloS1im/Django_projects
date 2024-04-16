from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm

from django.conf import settings
from django.core.mail import send_mail
from products.models import Basket,BasketQuerySet,Product,SizeSelected,Favorites,FavoritesQuerySet





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
        'footer_1': "127015, Москва, Бумажный пр-д., д. 14, стр. 2 ООО «НИКАМЕД».",
        'footer_2': "Копирование материалов запрещено.",
        'form': form,
    }

    return render(request,'users/index.html',context)

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            created_user = User.objects.last()
            password = User.objects.make_random_password()
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
                'footer_1': "127015, Москва, Бумажный пр-д., д. 14, стр. 2 ООО «НИКАМЕД».",
                'footer_2': "Копирование материалов запрещено.",
                'form': form
            }
            print(form.errors)
            return render(request, 'users/registration.html', context)
    form = UserRegistrationForm()
    context = {
        'title': "Регирстрация",
        'header': "Регистрация",
        'form_label': "Регистрация",
        'footer_1': "127015, Москва, Бумажный пр-д., д. 14, стр. 2 ООО «НИКАМЕД».",
        'footer_2': "Копирование материалов запрещено.",
        'form': form,
    }
    return render(request, 'users/registration.html', context)

def registration_confirm(request):
    context = {
        'title': "Подтверждение регистрации",
        'header': "Подтверждение регистрации",
        'form_label': "Вы успешно зарегистрированы. Пароль отправлен на вашу почту. Введите почту и пароль на главной странице для входа на сайт.",
        'footer_1': "127015, Москва, Бумажный пр-д., д. 14, стр. 2 ООО «НИКАМЕД».",
        'footer_2': "Копирование материалов запрещено."
    }
    return render(request, 'users/registration_confirm.html', context)


def recovery(request):
    context = {
        'title': "Восстановление данных",
        'header': "Восстановление данных",
        'form_label': "Восстановить пароль",
        'footer_1': "127015, Москва, Бумажный пр-д., д. 14, стр. 2 ООО «НИКАМЕД».",
        'footer_2': "Копирование материалов запрещено."
    }
    return render(request, 'users/recovery.html', context)

def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    baskets = Basket.objects.filter(user=request.user)
    favorites = Favorites.objects.filter(user=request.user).order_by('product')
    context = {
        'title': "Личный кабинет",
        'footer_1': "127015, Москва, Бумажный пр-д., д. 14, стр. 2 ООО «НИКАМЕД».",
        'footer_2': "Копирование материалов запрещено.",
        'form': form,
        'baskets': baskets,
        'favorites': favorites,
    }
    return render(request, 'users/profile.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:index'))


