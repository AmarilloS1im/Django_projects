from django import forms
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm, PasswordChangeForm)
from django.utils.translation import gettext_lazy as _

from .models import User, Image
from django import forms
from image_cropping import ImageCropWidget


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': 'Email/Почта', 'name': 'email',
        'type': 'email'
    }))
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        required=False
    )

    class Meta:
        model = User
        fields = ('email',)


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(required=False)
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': 'Email/Почта', 'name': 'email',
        'type': 'email'
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': 'Password/Пароль', 'name': 'password',
        'type': 'password'
    }))

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    class Meta:
        model = User
        fields = ('email', 'password')


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input', 'type': 'text', 'name': 'username', 'placeholder': 'Имя Пользователя',
        'id': 'username_id'
    }), required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input', 'type': 'text', 'name': 'first_name', 'placeholder': 'Имя', 'id': 'first_name_id'
    }), required=False)

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input', 'type': 'text', 'name': 'last_name', 'placeholder': 'Фамилия', 'id': 'last_name_id'
    }), required=False)

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-input', 'type': 'email', 'name': 'email', 'placeholder': 'Эл.Почта', 'readonly': True,
        'style': 'color:#C0BFBF;', 'id': 'user_email_id',
    }))

    image = forms.ImageField(widget=forms.FileInput(attrs={
        'type': 'file', 'name': 'file', 'accept': 'image/*', 'id': 'id_file',
    }), required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'image',)


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('file',)


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(
        attrs={'class': 'input', 'placeholder': 'Старый пароль'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(
        attrs={'class': 'input', 'placeholder': 'Новый пароль'}))
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(
        attrs={'class': 'input', 'placeholder': 'Новый пароль еще раз'}))
