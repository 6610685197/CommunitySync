from django import forms
from django.forms import inlineformset_factory
from .models import Visitor, VisitorImage
from apps.accounts.models import CustomUser


_input = "w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
_select = _input + " bg-white"

class VisitorForm(forms.ModelForm):
    resident = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role="resident").order_by("username"),
        label="Visiting Resident",
        widget=forms.Select(attrs={"class": _select}),
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
            "name": forms.TextInput(attrs={"class": _input, "placeholder": "Visitor full name or nickname"}),
            "home_number": forms.TextInput(attrs={"class": _input, "placeholder": "e.g. 12A or Room 302"}),
            "address": forms.Textarea(attrs={"class": _input, "rows": 2, "placeholder": "Visitor's home address"}),
            "license_plate": forms.TextInput(attrs={"class": _input, "placeholder": "e.g. กข 1234 (optional)"}),
            "visit_time": forms.DateTimeInput(attrs={"class": _input, "type": "datetime-local"}),
            "status": forms.Select(attrs={"class": _select}),
            "note": forms.Textarea(attrs={"class": _input, "rows": 2, "placeholder": "Any additional notes (optional)"}),
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