from django import forms
from django.forms import inlineformset_factory
from .models import Visitor, VisitorImage
from apps.accounts.models import CustomUser


class VisitorForm(forms.ModelForm):
    resident = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role="resident").order_by("username"),
        label="Visit Resident",
    )

    class Meta:
        model = Visitor
        fields = [
            "name",
            "resident",
            "home_number",
            "address",
            "license_plate",
            "visit_time",
            "status",
            "note",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Visitor name or nickname"}),
            "home_number": forms.TextInput(attrs={"placeholder": "Home number / room number"}),
            "address": forms.Textarea(attrs={"rows": 3, "placeholder": "Address"}),
            "license_plate": forms.TextInput(attrs={"placeholder": "Optional"}),
            "visit_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "note": forms.Textarea(attrs={"rows": 3, "placeholder": "Optional note"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        resident = cleaned_data.get("resident")
        address = cleaned_data.get("address")

        if resident and not address:
            cleaned_data["address"] = resident.address

        return cleaned_data


VisitorImageFormSet = inlineformset_factory(
    Visitor,
    VisitorImage,
    fields=["image"],
    extra=3,
    can_delete=True,
)