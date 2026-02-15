from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # Roles defined in your Requirement & Mapping documents [cite: 106, 109]
    ROLE_CHOICES = (
        ("resident", "Resident"),
        ("juristic", "Juristic Person"),
        ("security", "Security Staff"),
    )

    # Fields from your Class Diagram [cite: 39]
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="resident")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    car_plate_num = models.CharField(max_length=20, blank=True, null=True)

    # Resident specific field [cite: 39]
    address = models.TextField(
        blank=True, null=True, help_text="Required for Residents"
    )

    # Use email as the primary login field if preferred, otherwise default is username
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "name", "role"]

    def __str__(self):
        return f"{self.username} ({self.role})"
