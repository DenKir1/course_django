from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page

from users.apps import UsersConfig
from users.views import RegisterView, UserUpdateView, UserListView, VerifyView, get_password, logout_view

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('profile/<int:pk>/', UserUpdateView.as_view(), name='profile'),
    path('users_list/', UserListView.as_view(), name='users_list'),
    path('get_password/', get_password, name='get_password'),

    ]
