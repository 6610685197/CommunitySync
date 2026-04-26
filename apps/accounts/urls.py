from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("create-account/", views.create_account, name="create_account"),
    path("auth/oauth/", views.oauth_auth, name="auth_discord"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("home/", views.index, name="index"),
    path("users/", views.user_list, name="user_list"),
    path("security-dashboard/", views.security_dashboard, name="security_dashboard"),
]
