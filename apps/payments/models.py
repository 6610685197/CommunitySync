from decimal import Decimal
from django.db import models
from django.conf import settings


class FeeType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class BillingRule(models.Model):
    CYCLE_CHOICES = (
        ("one_time", "One Time"),
        ("monthly", "Monthly"),
        ("manual", "Manual"),
    )

    TARGET_CHOICES = (
        ("all", "All Residents"),
        ("selected", "Selected Residents"),
    )

    name = models.CharField(max_length=150)
    fee_type = models.ForeignKey(FeeType, on_delete=models.PROTECT, related_name="rules")
    cycle = models.CharField(max_length=20, choices=CYCLE_CHOICES, default="monthly")
    target_type = models.CharField(max_length=20, choices=TARGET_CHOICES, default="all")
    default_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class BillingRuleResident(models.Model):
    rule = models.ForeignKey(BillingRule, on_delete=models.CASCADE, related_name="rule_residents")
    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "resident"},
    )

    class Meta:
        unique_together = ("rule", "resident")

    def __str__(self):
        return f"{self.rule.name} -> {self.resident.username}"


class Bill(models.Model):
    STATUS_CHOICES = (
        ("unpaid", "Unpaid"),
        ("pending_review", "Pending Review"),
        ("paid", "Paid"),
        ("rejected", "Rejected"),
        ("overdue", "Overdue"),
    )

    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bills",
        limit_choices_to={"role": "resident"},
    )
    fee_type = models.ForeignKey(FeeType, on_delete=models.PROTECT, related_name="bills")
    billing_rule = models.ForeignKey(
        BillingRule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bills",
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()

    billing_month = models.PositiveIntegerField(null=True, blank=True)
    billing_year = models.PositiveIntegerField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="unpaid")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_bills",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def latest_receipt(self):
        return self.receipts.order_by("-created_at").first()

    def __str__(self):
        return f"{self.title} - {self.resident.username}"


class PaymentReceipt(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="receipts")
    receipt_image = models.ImageField(upload_to="payment_receipts/")
    note = models.TextField(blank=True, null=True)

    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="submitted_payment_receipts",
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_payment_receipts",
    )
    review_note = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Receipt for {self.bill.title}"