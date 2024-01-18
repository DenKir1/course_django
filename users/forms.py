from users.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'phone', 'password1', 'password2',)


class UpdateForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class ModeratorForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
