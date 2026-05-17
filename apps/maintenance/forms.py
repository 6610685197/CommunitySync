from django import forms
from .models import MaintenanceRequest

_input = "w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
_select = _input + " bg-white"


class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ["title", "description", "request_type", "location_detail"]
        widgets = {
            "title": forms.TextInput(attrs={"class": _input, "placeholder": "Brief title of the issue"}),
            "description": forms.Textarea(attrs={"class": _input, "rows": 4, "placeholder": "Describe the problem in detail…"}),
            "request_type": forms.Select(attrs={"class": _select}),
            "location_detail": forms.TextInput(attrs={"class": _input, "placeholder": "e.g. Building A lobby / House 23"}),
        }


class MaintenanceStatusForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ["status"]
        widgets = {
            "status": forms.Select(attrs={"class": _select}),
        }