from django.urls import path
from . import views

urlpatterns = [
    path("", views.bill_list, name="bill_list"),
    path("bill/<int:pk>/", views.bill_detail, name="bill_detail"),
    path("bill/create/", views.bill_create, name="bill_create"),
    path("bill/<int:pk>/edit/", views.bill_update, name="bill_update"),
    path("bill/<int:pk>/delete/", views.bill_delete, name="bill_delete"),

    path("bill/<int:pk>/upload-receipt/", views.upload_receipt, name="upload_receipt"),
    path("receipt/<int:receipt_id>/review/", views.review_receipt, name="review_receipt"),

    path("billing-rules/", views.billing_rule_list, name="billing_rule_list"),
    path("billing-rules/create/", views.billing_rule_create, name="billing_rule_create"),
    path("billing-rules/<int:rule_id>/generate/", views.generate_bills_from_rule, name="generate_bills_from_rule"),
]