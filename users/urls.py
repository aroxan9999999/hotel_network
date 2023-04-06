from django.urls import path, include
from .views import UserRegister, UserLogin, logout_view


urlpatterns = [
    path('register', UserRegister.as_view(), name='register'),
    path('login', UserLogin.as_view(), name='login'),
    path('logaut', logout_view, name='logaut'),
]
