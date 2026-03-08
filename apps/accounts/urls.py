from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("auth/discord/", views.discord_auth, name="auth_discord"),
    path("create-account/", views.create_account, name="create_account"),
    # Destination URLs
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("home/", views.resident_home, name="resident_home"),
    path("", views.index, name="index"),
    path("users/", views.user_list, name="user_list"),
]