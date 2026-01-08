from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.user_dashboard, name="user_dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),

    path("profile/", views.profile, name="profile"),
    path("audit-logs/", views.audit_logs, name="audit_logs"),
]
