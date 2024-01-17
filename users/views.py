from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from users.forms import RegisterForm, ModeratorForm, UpdateForm
from users.models import User


#class UserLoginView(LoginView):
#    template_name = 'users/login.html'


#class UserLogoutView(LogoutView):
#    pass


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.save()
        verify_code = User.objects.make_random_password(length=15)
        new_user.verify_code = verify_code
        new_user.save()
        try:
            send_mail(
                subject='Подтверждение регистрации',
                message=f' Для получения полного доступа, введите код верификации: {verify_code}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[new_user.email]
            )
        except:
            Exception
        print(f'{new_user} Введите код верификации: {verify_code}')
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_class(self):
        if self.request.user.has_perm('users.set_is_active'):
            return ModeratorForm
        else:
            return UpdateForm

    def form_valid(self, form):
        verify_user = self.object
        verify_pass = verify_user.verify_pass
        verify_code = verify_user.verify_code
        if not verify_user.is_verify:
            if verify_code == verify_pass:
                verify_user.is_verify = True
                verify_user.save()
                print('Верификация прошла успешно')
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    extra_context = {'title': 'Пользователи', }

    def test_func(self):
        _user = self.request.user
        if _user.has_perms('users.set_is_active'):
            return True
        return self.handle_no_permission()
