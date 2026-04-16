from django import forms
from .models import MaintenanceRequest


class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ["title", "description", "request_type", "location_detail"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Request title"}),
            "description": forms.Textarea(attrs={"rows": 5, "placeholder": "Describe the problem"}),
            "request_type": forms.Select(),
            "location_detail": forms.TextInput(attrs={"placeholder": "Example: Building A lobby / House 23"}),
        }


class MaintenanceStatusForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ["status"]
        widgets = {
            "status": forms.Select(),
        }