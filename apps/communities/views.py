from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FacilityBookingForm, FacilityForm, FacilityUnitForm
from .models import Facility, FacilityBooking, FacilityUnit


def is_juristic(user):
    return user.is_authenticated and user.role == "juristic"


def is_resident(user):
    return user.is_authenticated and user.role == "resident"


@login_required
def facility_list(request):
    facilities = Facility.objects.all()

    if request.user.role == "resident":
        facilities = facilities.filter(is_active=True)

    return render(request, "communities/facility_list.html", {
        "facilities": facilities
    })


@login_required
def facility_detail(request, pk):
    facility = get_object_or_404(Facility, pk=pk)

    if request.user.role == "resident" and not facility.is_active:
        return HttpResponseForbidden("This facility is not available.")

    units = facility.units.all()

    return render(request, "communities/facility_detail.html", {
        "facility": facility,
        "units": units,
    })


@login_required
def facility_create(request):
    if not is_juristic(request.user):
        return HttpResponseForbidden("Only juristic can create facility.")

    if request.method == "POST":
        form = FacilityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Facility created successfully.")
            return redirect("facility_list")
    else:
        form = FacilityForm()

    return render(request, "communities/facility_form.html", {
        "form": form,
        "page_title": "Create Facility",
    })


@login_required
def facility_update(request, pk):
    if not is_juristic(request.user):
        return HttpResponseForbidden("Only juristic can edit facility.")

    facility = get_object_or_404(Facility, pk=pk)

    if request.method == "POST":
        form = FacilityForm(request.POST, request.FILES, instance=facility)
        if form.is_valid():
            form.save()
            messages.success(request, "Facility updated successfully.")
            return redirect("facility_detail", pk=facility.pk)
    else:
        form = FacilityForm(instance=facility)

    return render(request, "communities/facility_form.html", {
        "form": form,
        "page_title": "Edit Facility",
    })


@login_required
def facility_delete(request, pk):
    if not is_juristic(request.user):
        return HttpResponseForbidden("Only juristic can delete facility.")

    facility = get_object_or_404(Facility, pk=pk)

    if request.method == "POST":
        facility.delete()
        messages.success(request, "Facility deleted successfully.")
        return redirect("facility_list")

    return render(request, "communities/facility_confirm_delete.html", {
        "facility": facility
    })


@login_required
def facility_unit_list(request):
    if not is_juristic(request.user):
        return HttpResponseForbidden("Only juristic can manage units.")

    units = FacilityUnit.objects.select_related("facility").all()
    return render(request, "communities/facility_unit_list.html", {
        "units": units
    })


@login_required
def facility_unit_create(request, facility_id):
    if not is_juristic(request.user):
        return HttpResponseForbidden("Only juristic can create units.")

    facility = get_object_or_404(Facility, pk=facility_id)

    if not facility.requires_booking:
        messages.error(request, "This facility does not require booking.")
        return redirect("facility_detail", pk=facility.pk)

    if request.method == "POST":
        form = FacilityUnitForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.facility = facility
            unit.save()
            messages.success(request, "Facility unit created successfully.")
            return redirect("facility_detail", pk=facility.pk)
    else:
        form = FacilityUnitForm()

    return render(request, "communities/facility_unit_form.html", {
        "form": form,
        "page_title": f"Add Unit for {facility.name}",
        "facility": facility,
    })


@login_required
def facility_unit_update(request, pk):
    if not is_juristic(request.user):
        return HttpResponseForbidden("Only juristic can edit units.")

    unit = get_object_or_404(FacilityUnit, pk=pk)

    if request.method == "POST":
        form = FacilityUnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            messages.success(request, "Facility unit updated successfully.")
            return redirect("facility_detail", pk=unit.facility.pk)
    else:
        form = FacilityUnitForm(instance=unit)

    return render(request, "communities/facility_unit_form.html", {
        "form": form,
        "page_title": f"Edit Unit for {unit.facility.name}",
        "facility": unit.facility,
    })


@login_required
def facility_unit_delete(request, pk):
    if not is_juristic(request.user):
        return HttpResponseForbidden("Only juristic can delete units.")

    unit = get_object_or_404(FacilityUnit, pk=pk)
    facility_pk = unit.facility.pk

    if request.method == "POST":
        unit.delete()
        messages.success(request, "Facility unit deleted successfully.")
        return redirect("facility_detail", pk=facility_pk)

    return render(request, "communities/facility_unit_confirm_delete.html", {
        "unit": unit
    })


@login_required
def facility_booking_list(request):
    if is_juristic(request.user):
        bookings = FacilityBooking.objects.select_related(
            "resident", "facility_unit", "facility_unit__facility"
        ).all()
    elif is_resident(request.user):
        bookings = FacilityBooking.objects.select_related(
            "resident", "facility_unit", "facility_unit__facility"
        ).filter(resident=request.user)
    else:
        return HttpResponseForbidden("No permission.")

    return render(request, "communities/facility_booking_list.html", {
        "bookings": bookings
    })


@login_required
def facility_booking_create(request, unit_id):
    if not is_resident(request.user):
        return HttpResponseForbidden("Only residents can book.")

    unit = get_object_or_404(FacilityUnit.objects.select_related("facility"), pk=unit_id)

    if not unit.facility.requires_booking:
        return HttpResponseForbidden("This facility does not require booking.")

    if unit.status != "available":
        messages.error(request, "This unit is not available for booking.")
        return redirect("facility_detail", pk=unit.facility.pk)

    if request.method == "POST":
        form = FacilityBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.resident = request.user
            booking.facility_unit = unit
            booking.status = "approved"
            booking.save()

            unit.status = "booked"
            unit.save()

            messages.success(request, "Booking created successfully.")
            return redirect("facility_booking_list")
    else:
        form = FacilityBookingForm()

    return render(request, "communities/facility_booking_form.html", {
        "form": form,
        "unit": unit,
        "facility": unit.facility,
    })


@login_required
def facility_booking_cancel(request, pk):
    booking = get_object_or_404(FacilityBooking.objects.select_related("facility_unit"), pk=pk)

    if is_resident(request.user):
        if booking.resident != request.user:
            return HttpResponseForbidden("No permission.")
    elif not is_juristic(request.user):
        return HttpResponseForbidden("No permission.")

    if request.method == "POST":
        booking.status = "cancelled"
        booking.save()

        unit = booking.facility_unit
        if unit.status == "booked":
            unit.status = "available"
            unit.save()

        messages.success(request, "Booking cancelled successfully.")
        return redirect("facility_booking_list")

    return render(request, "communities/facility_booking_confirm_cancel.html", {
        "booking": booking
    })