
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from users.forms import RegisterForm, ModeratorForm, UpdateForm
from users.models import User
from users.services import send_sms, send_mail_user


# class UserLogoutView(LogoutView): # Не работает
#    success_url = reverse_lazy('users:login')
def logout_view(request):
    logout(request)
    return redirect('users:login')


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verify')

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.save()
        verify_code = User.objects.make_random_password(length=15)
        verify_phone = User.objects.make_random_password(length=15)
        new_user.verify_code = verify_code
        new_user.verify_phone = verify_phone
        new_user.save()
        result_send = send_mail_user(
            subject='Подтверждение регистрации',
            message=f' Для получения полного доступа, введите код активации: {verify_code}',
            email_list=[new_user.email]
        )

        result_sms = send_sms(phone=new_user.phone, message=verify_phone)

        print(result_send, result_sms, sep='\n\n')
        print(f'{new_user} Введите код активации: {verify_code}')
        print(f'{new_user.phone} код верификации: {verify_phone}')
        return super().form_valid(form)


class VerifyView(TemplateView):
    template_name = 'users/verify.html'

    @staticmethod
    def post(request):
        verify_pass = request.POST.get('verify_pass')
        user_code = User.objects.filter(verify_code=verify_pass).first()
        user_phone = User.objects.filter(verify_phone=verify_pass).first()
        if user_code:
            user_code.is_active = True
            user_code.save()
            result_send = send_mail_user(
                                subject='Успешная активация',
                                message='Код активации принят',
                                email_list=[user_code.email]
                        )
            print(result_send)
            return redirect('users:login')
        if user_phone:
            user_phone.is_verify = True
            user_phone.save()
            result_sms = send_sms(phone=user_phone.phone, message='Welcome')
            print(f'Верификация телефона {user_phone.phone} прошла успешно')
            print(result_sms)
            return redirect('users:login')
        else:
            return redirect('users:verify')


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    success_url = reverse_lazy('users:login')

    def test_func(self):
        _user = self.request.user
        if self.request.user == self.get_object() or _user.has_perms(['users.set_is_active', ]):
            return True
        return self.handle_no_permission()

    def get_form_class(self):
        if self.request.user == self.get_object():
            return UpdateForm
        elif self.request.user.has_perm('users.set_is_active'):
            return ModeratorForm


def get_password(request):
    new_pass = request.user.objects.make_random_password(length=15)
    result_send = send_mail_user(
        subject='Новый пароль',
        message=f'Новый пароль {new_pass}',
        email_list=[request.user.email]
    )

    if result_send:
        request.user.set_password(new_pass)
        request.user.save()
        print(f'{request.user.email} - получил новый пароль - {new_pass}')
    else:
        print(f'{request.user.email} не удалось изменить пароль')

    return redirect(reverse('users:login'))


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    extra_context = {'title': 'Пользователи', }

    def test_func(self):
        _user = self.request.user
        if _user.has_perms(['users.set_is_active', ]):
            return True
        return self.handle_no_permission()
