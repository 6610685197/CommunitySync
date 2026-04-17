from django import forms
from .models import BillingRule, Bill, PaymentReceipt


class BillingRuleForm(forms.ModelForm):
    class Meta:
        model = BillingRule
        fields = ["name", "cycle", "target_type", "default_amount", "is_active"]


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = [
            "resident",
            "name",
            "title",
            "description",
            "amount",
            "due_date",
            "billing_month",
            "billing_year",
            "status",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }


class PaymentReceiptForm(forms.ModelForm):
    class Meta:
        model = PaymentReceipt
        fields = ["receipt_image", "note"]


class PaymentReceiptReviewForm(forms.ModelForm):
    class Meta:
        model = PaymentReceipt
        fields = ["status", "review_note"]