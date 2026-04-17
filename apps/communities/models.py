from django.db import models
from django.conf import settings


class Facility(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="facility_images/", blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    requires_booking = models.BooleanField(default=False)
    booking_note = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class FacilityUnit(models.Model):
    STATUS_CHOICES = (
        ("available", "Available"),
        ("booked", "Booked"),
        ("closed_maintenance", "Closed (Maintenance)"),
        ("closed_investigate", "Closed (Investigate)"),
        ("closed_rearrange", "Closed (Re-arrange)"),
    )

    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="units"
    )
    unit_name = models.CharField(max_length=150)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="available")
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("facility", "unit_name")
        ordering = ["facility__name", "unit_name"]

    def __str__(self):
        return f"{self.facility.name} - {self.unit_name}"


class FacilityBooking(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
    )

    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="facility_bookings",
        limit_choices_to={"role": "resident"},
    )
    facility_unit = models.ForeignKey(
        FacilityUnit,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-booking_date", "start_time"]

    def __str__(self):
        return f"{self.resident.username} - {self.facility_unit.unit_name}"