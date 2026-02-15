from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # Destination URLs
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("home/", views.resident_home, name="resident_home"),
]
