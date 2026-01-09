from django.contrib.auth import login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


@login_required
def profile(request):
    user = request.user
    return render(request, "accounts/profile.html", {
        "username": user.username,
        "email": user.email,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "last_login": user.last_login,
        "date_joined": user.date_joined,
    })


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_password1(self):
        pw = self.cleaned_data.get("password1")

        #Trigger Django's AUTH_PASSWORD_VALIDATORS
        validate_password(pw, self.instance)

        #Optional extra rules
        if not any(c.isdigit() for c in pw):
            raise forms.ValidationError("Password must include at least 1 number.")
        if not any(c.isupper() for c in pw):
            raise forms.ValidationError("Password must include at least 1 uppercase letter.")

        return pw


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  #This is important
            messages.success(request, "Account created. Please login.")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        #If user already login, send to role
        if request.user.is_staff:
            return redirect("admin_dashboard")
        return redirect("user_dashboard")

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_staff:
                return redirect("admin_dashboard")
            return redirect("user_dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def user_dashboard(request):
    return render(request, 'accounts/user_dashboard.html')


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        raise PermissionDenied
    return render(request, 'accounts/admin_dashboard.html')

@login_required
def audit_logs(request):
    if not request.user.is_staff:
        raise PermissionDenied
    with open("audit.log", "r") as f:
        lines = f.readlines()[-200:]
    return render(request, "accounts/audit_logs.html", {"lines": lines})

