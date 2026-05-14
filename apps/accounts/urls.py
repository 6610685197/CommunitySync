from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("create-account/", views.create_account, name="create_account"),
    path("auth/oauth/", views.oauth_auth, name="auth_discord"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("home/", views.index, name="index"),
    path("users/", views.user_list, name="user_list"),
    path("security-dashboard/", views.security_dashboard, name="security_dashboard"),
    # Password Recovery
    path("forgot-password/", views.forgot_password_view, name="forgot_password"),
    path("forgot-password/verify-otp/", views.verify_otp_view, name="verify_otp"),
    path("forgot-password/verify-plate/", views.verify_plate_view, name="verify_plate"),
    path("reset-password/", views.reset_password_view, name="reset_password"),
    path("link-account/", views.link_account_view, name="link_account"),
]
