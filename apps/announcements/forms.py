from django import forms
from .models import Announcement

_input = "w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": _input, "placeholder": "Enter announcement title"}),
            "content": forms.Textarea(attrs={"class": _input, "rows": 6, "placeholder": "Write the full announcement here…"}),
        }