from django import forms
from .models import Announcement


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter announcement title"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter announcement content",
                "rows": 6
            }),
        }