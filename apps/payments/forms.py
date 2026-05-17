from django import forms
from .models import BillingRule, Bill, PaymentReceipt


_input = "w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
_select = _input + " bg-white"

class BillingRuleForm(forms.ModelForm):
    class Meta:
        model = BillingRule
        fields = ["name", "cycle", "target_type", "default_amount", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": _input, "placeholder": "e.g. Monthly Maintenance Fee"}),
            "cycle": forms.Select(attrs={"class": _select}),
            "target_type": forms.Select(attrs={"class": _select, "id": "id_target_type"}),
            "default_amount": forms.NumberInput(attrs={"class": _input, "placeholder": "0.00", "step": "0.01", "min": "0"}),
            "is_active": forms.CheckboxInput(attrs={"class": "h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"}),
        }


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
            "resident": forms.Select(attrs={"class": _select}),
            "name": forms.TextInput(attrs={"class": _input, "placeholder": "e.g. Monthly Fee"}),
            "title": forms.TextInput(attrs={"class": _input, "placeholder": "e.g. January 2025 Maintenance"}),
            "description": forms.Textarea(attrs={"class": _input, "rows": 3, "placeholder": "Optional details about this bill…"}),
            "amount": forms.NumberInput(attrs={"class": _input, "placeholder": "0.00", "step": "0.01", "min": "0"}),
            "due_date": forms.DateInput(attrs={"type": "date", "class": _input}),
            "billing_month": forms.NumberInput(attrs={"class": _input, "placeholder": "1 – 12", "min": "1", "max": "12"}),
            "billing_year": forms.NumberInput(attrs={"class": _input, "placeholder": "e.g. 2025"}),
            "status": forms.Select(attrs={"class": _select}),
        }


class PaymentReceiptForm(forms.ModelForm):
    class Meta:
        model = PaymentReceipt
        fields = ["receipt_image", "note"]
        widgets = {
            "note": forms.Textarea(attrs={"class": _input, "rows": 2, "placeholder": "Optional note for the reviewer…"}),
        }


class PaymentReceiptReviewForm(forms.ModelForm):
    class Meta:
        model = PaymentReceipt
        fields = ["status", "review_note"]
        widgets = {
            "status": forms.Select(attrs={"class": _select}),
            "review_note": forms.Textarea(attrs={"class": _input, "rows": 3, "placeholder": "Leave a note for the resident (optional)…"}),
        }