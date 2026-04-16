from django.urls import path
from . import views

urlpatterns = [
    path("resident/", views.resident_dashboard, name="resident_dashboard"),
]