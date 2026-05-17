from django.db import models
from django.conf import settings


class Visitor(models.Model):
    STATUS_CHOICES = (
        ("expected", "Expected"),
        ("arrived", "Arrived"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("completed", "Completed"),
    )

    # Visitor basic info
    name = models.CharField(max_length=255, help_text="Can be full name or nickname")
    license_plate = models.CharField(max_length=50, blank=True, null=True)

    # Who the visitor is visiting
    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="visitors",
        limit_choices_to={"role": "resident"},
    )

    # Snapshot info for convenience
    home_number = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)

    # Optional details
    note = models.TextField(blank=True, null=True)
    visit_time = models.DateTimeField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="expected")

    # Audit
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_visitors",
        limit_choices_to={"role": "security"},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} -> {self.resident.username}"


class VisitorImage(models.Model):
    visitor = models.ForeignKey(
        Visitor,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="visitor_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.visitor.name}"