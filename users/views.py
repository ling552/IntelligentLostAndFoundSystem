from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import LoginForm, ProfileForm, RegisterForm


class UserLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = LoginForm


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "注册成功，欢迎加入。")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "账户信息已更新。")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "users/profile.html", {"form": form})
