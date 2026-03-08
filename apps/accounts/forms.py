from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "name",
            "email",
            "role",
            "phone_number",
            "car_plate_num",
            "address",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only allow juristic to create these roles from this page
        self.fields["role"].choices = [
            ("resident", "Resident"),
            ("security", "Security Staff"),
            ("juristic", "Juristic Person"),
        ]

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        address = cleaned_data.get("address")

        if role == "resident" and not address:
            self.add_error("address", "Address is required for residents.")

        if role == "security":
            cleaned_data["address"] = ""

        return cleaned_data