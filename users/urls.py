from django.urls import path

from .views import UserLoginView, UserLogoutView, profile, register

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
    path("me/profile/", profile, name="profile"),
]
