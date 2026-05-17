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

_input = "w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
_select = _input + " bg-white"

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
        widgets = {
            "username": forms.TextInput(attrs={"class": _input, "placeholder": "e.g. john_doe"}),
            "name": forms.TextInput(attrs={"class": _input, "placeholder": "Full name"}),
            "email": forms.EmailInput(attrs={"class": _input, "placeholder": "email@example.com"}),
            "role": forms.Select(attrs={"class": _select}),
            "phone_number": forms.TextInput(attrs={"class": _input, "placeholder": "e.g. 081-234-5678"}),
            "car_plate_num": forms.TextInput(attrs={"class": _input, "placeholder": "e.g. กข 1234"}),
            "address": forms.Textarea(attrs={"class": _input, "rows": 2, "placeholder": "House number, street, unit…"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["role"].choices = [
            ("resident", "Resident"),
            ("security", "Security Staff"),
            ("juristic", "Juristic Person"),
        ]
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={"class": _input, "placeholder": "Enter password"}
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"class": _input, "placeholder": "Confirm password"}
        )

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        address = cleaned_data.get("address")

        if role == "resident" and not address:
            self.add_error("address", "Address is required for residents.")

        if role == "security":
            cleaned_data["address"] = ""

        return cleaned_data