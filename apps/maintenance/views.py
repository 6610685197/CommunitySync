from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import MaintenanceRequest
from .forms import MaintenanceRequestForm, MaintenanceStatusForm


@login_required
def maintenance_list(request):
    if request.user.role == "juristic":
        requests = MaintenanceRequest.objects.select_related("resident", "created_by").all()
    elif request.user.role == "resident":
        requests = MaintenanceRequest.objects.select_related("resident", "created_by").filter(resident=request.user)
    else:
        return HttpResponseForbidden("You do not have permission to access maintenance requests.")

    return render(request, "maintenance/maintenance_list.html", {
        "requests": requests
    })


@login_required
def maintenance_detail(request, pk):
    try:
        req = MaintenanceRequest.objects.select_related("resident", "created_by").get(pk=pk)
    except MaintenanceRequest.DoesNotExist:
        messages.error(request, "The requested maintenance request no longer exists.")
        return redirect("maintenance_list")

    if request.user.role == "juristic":
        pass
    elif request.user.role == "resident":
        if req.resident != request.user:
            return HttpResponseForbidden("You do not have permission to view this request.")
    else:
        return HttpResponseForbidden("You do not have permission to view this request.")

    return render(request, "maintenance/maintenance_detail.html", {
        "req": req
    })


@login_required
def maintenance_create(request):
    if request.user.role not in ["resident", "juristic"]:
        return HttpResponseForbidden("You do not have permission to create requests.")

    if request.method == "POST":
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.created_by = request.user

            # resident auto assign
            if request.user.role == "resident":
                req.resident = request.user
                if hasattr(request.user, "address"):
                    req.location_detail = req.location_detail or request.user.address

            # juristic can create common-area request without resident
            elif request.user.role == "juristic":
                req.resident = None

            req.save()
            return redirect("maintenance_list")
    else:
        form = MaintenanceRequestForm()

    return render(request, "maintenance/maintenance_form.html", {
        "form": form,
        "page_title": "Create Maintenance Request",
    })


@login_required
def maintenance_update_status(request, pk):
    if request.user.role != "juristic":
        return HttpResponseForbidden("Only juristic can update request status.")

    req = get_object_or_404(MaintenanceRequest, pk=pk)

    if request.method == "POST":
        form = MaintenanceStatusForm(request.POST, instance=req)
        if form.is_valid():
            form.save()
            return redirect("maintenance_detail", pk=req.pk)
    else:
        form = MaintenanceStatusForm(instance=req)

    return render(request, "maintenance/maintenance_status_form.html", {
        "form": form,
        "req": req,
    })