from django import forms
from .models import Facility, FacilityUnit, FacilityBooking

_input = "w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
_select = _input + " bg-white"
_check = "h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"


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
            "name": forms.TextInput(attrs={"class": _input, "placeholder": "e.g. Swimming Pool"}),
            "description": forms.Textarea(attrs={"class": _input, "rows": 4, "placeholder": "Describe this facility…"}),
            "location": forms.TextInput(attrs={"class": _input, "placeholder": "e.g. Building A, Ground Floor"}),
            "requires_booking": forms.CheckboxInput(attrs={"class": _check, "id": "id_requires_booking"}),
            "booking_note": forms.Textarea(attrs={"class": _input, "rows": 3, "placeholder": "Instructions or rules for booking this facility…"}),
            "is_active": forms.CheckboxInput(attrs={"class": _check}),
        }


class FacilityUnitForm(forms.ModelForm):
    class Meta:
        model = FacilityUnit
        fields = ["unit_name", "status", "note"]
        widgets = {
            "unit_name": forms.TextInput(attrs={"class": _input, "placeholder": "e.g. Lane 1 or Court A"}),
            "status": forms.Select(attrs={"class": _select}),
            "note": forms.Textarea(attrs={"class": _input, "rows": 3, "placeholder": "Optional note about this unit…"}),
        }


class FacilityBookingForm(forms.ModelForm):
    class Meta:
        model = FacilityBooking
        fields = ["booking_date", "start_time", "end_time", "note"]
        widgets = {
            "booking_date": forms.DateInput(attrs={"class": _input, "type": "date"}),
            "start_time": forms.TimeInput(attrs={"class": _input, "type": "time"}),
            "end_time": forms.TimeInput(attrs={"class": _input, "type": "time"}),
            "note": forms.Textarea(attrs={"class": _input, "rows": 3, "placeholder": "Any special requests or notes…"}),
        }