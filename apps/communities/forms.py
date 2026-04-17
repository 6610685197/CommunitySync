from django import forms
from .models import Facility, FacilityUnit, FacilityBooking


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = [
            "name",
            "description",
            "image",
            "location",
            "requires_booking",
            "booking_note",
            "is_active",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "booking_note": forms.Textarea(attrs={"rows": 3}),
        }


class FacilityUnitForm(forms.ModelForm):
    class Meta:
        model = FacilityUnit
        fields = ["unit_name", "status", "note"]
        widgets = {
            "note": forms.Textarea(attrs={"rows": 3}),
        }


class FacilityBookingForm(forms.ModelForm):
    class Meta:
        model = FacilityBooking
        fields = ["booking_date", "start_time", "end_time", "note"]
        widgets = {
            "booking_date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
            "note": forms.Textarea(attrs={"rows": 3}),
        }