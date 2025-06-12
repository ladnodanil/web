from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from gamestore.settings import DEFAULT_USER_IMAGE
from .forms import (
    LoginUserForm,
    RegisterUserForm,
    ProfileUserForm,
    UserPasswordChangeForm
)
from catalog.utils import DataMixin


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    title_page = 'Авторизация'


class RegisterUser(DataMixin, CreateView):
    success_url = reverse_lazy('users:login')
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    title_page = 'Регистрация'


class ProfileUser(DataMixin, LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    title_page = 'Профиль пользователя'
    extra_context = {'default_image': DEFAULT_USER_IMAGE}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(DataMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    title_page = "Изменение пароля"
