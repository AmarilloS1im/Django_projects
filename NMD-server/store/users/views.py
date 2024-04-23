from django.shortcuts import HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import CreateView, UpdateView, TemplateView, FormView
from store.utils import DataMixin


class IndexView(DataMixin, FormView):
    form_class = UserLoginForm
    template_name = 'users/index.html'
    title = "Вход/Регирстрация"
    header = "Сайт предзаказа для сотрудников"
    form_label = "Авторизация"

    def form_valid(self, form):
        email = self.request.POST['email']
        password = self.request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(self.request, user)
            return HttpResponseRedirect(reverse('products:products'))


class RegistrationView(DataMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    title = "Регирстрация"
    header = title
    form_label = header
    success_url = reverse_lazy('users:registration_confirm')

    def form_valid(self, form):
        form.save()
        created_user = User.objects.last()
        password = User.objects.make_random_password()
        created_user.set_password(password)
        created_user.save(update_fields=['password'])
        created_user.username = created_user.email
        created_user.save()
        print(password)
        send_mail('Ваш Пароль от сайта Никамед предзаказ',
                  f"ВАШ ПАРОЛЬ: {password}", settings.EMAIL_HOST_USER,
                  [f'{created_user.email}'])

        return super().form_valid(form)


class RegistrationConfirmView(DataMixin, TemplateView):
    template_name = 'users/registration_confirm.html'
    title = "Подтверждение регистрации"
    header = "Подтверждение регистрации"
    form_label = ("Вы успешно зарегистрированы. Пароль отправлен на вашу почту."
                  " Введите почту и пароль на главной странице для входа на сайт.")


class RecoveryView(DataMixin, TemplateView):
    template_name = 'users/recovery.html'
    title = "Восстановление данных"
    header = "Восстановление данных"
    form_label = "Восстановить пароль"


class ProfileView(DataMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = "Личный кабинет"

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:index'))
