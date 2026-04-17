from django.urls import path
from . import views

urlpatterns = [
    path("", views.facility_list, name="facility_list"),
    path("<int:pk>/", views.facility_detail, name="facility_detail"),

    path("create/", views.facility_create, name="facility_create"),
    path("<int:pk>/edit/", views.facility_update, name="facility_update"),
    path("<int:pk>/delete/", views.facility_delete, name="facility_delete"),

    path("units/", views.facility_unit_list, name="facility_unit_list"),
    path("<int:facility_id>/units/create/", views.facility_unit_create, name="facility_unit_create"),
    path("units/<int:pk>/edit/", views.facility_unit_update, name="facility_unit_update"),
    path("units/<int:pk>/delete/", views.facility_unit_delete, name="facility_unit_delete"),

    path("bookings/", views.facility_booking_list, name="facility_booking_list"),
    path("book/<int:unit_id>/", views.facility_booking_create, name="facility_booking_create"),
    path("bookings/<int:pk>/cancel/", views.facility_booking_cancel, name="facility_booking_cancel"),
]