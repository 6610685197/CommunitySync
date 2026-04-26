from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Visitor
from .forms import VisitorForm, VisitorImageFormSet


def is_security(user):
    return user.is_authenticated and user.role == "security"


def is_resident(user):
    return user.is_authenticated and user.role == "resident"


@login_required
def visitor_list(request):
    if request.user.role in ["security", "juristic"]:
        visitors = Visitor.objects.select_related("resident", "created_by").prefetch_related("images").order_by("-created_at")
    elif request.user.role == "resident":
        visitors = Visitor.objects.select_related("resident", "created_by").prefetch_related("images").filter(
            resident=request.user
        ).order_by("-created_at")
    else:
        return HttpResponseForbidden("You do not have permission to view visitors.")

    return render(request, "visitors/visitor_list.html", {"visitors": visitors})


@login_required
def visitor_detail(request, pk):
    visitor = get_object_or_404(
        Visitor.objects.select_related("resident", "created_by").prefetch_related("images"),
        pk=pk
    )

    if request.user.role == "security":
        pass
    elif request.user.role == "resident":
        if visitor.resident != request.user:
            return HttpResponseForbidden("You can only view your own visitors.")
    else:
        return HttpResponseForbidden("You do not have permission to view this visitor.")

    return render(request, "visitors/visitor_detail.html", {"visitor": visitor})


@login_required
def visitor_create(request):
    if request.user.role not in ["security", "juristic"]:
        return HttpResponseForbidden("Only security and juristic can add visitors.")

    if request.method == "POST":
        form = VisitorForm(request.POST)
        formset = VisitorImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            visitor = form.save(commit=False)

            # auto-fill address from resident if empty
            if not visitor.address and visitor.resident:
                visitor.address = visitor.resident.address

            visitor.created_by = request.user
            visitor.save()

            formset.instance = visitor
            formset.save()

            return redirect("visitor_list")
    else:
        form = VisitorForm()
        formset = VisitorImageFormSet()

    return render(request, "visitors/visitor_form.html", {
        "form": form,
        "formset": formset,
        "page_title": "Add Visitor",
    })


@login_required
def visitor_update(request, pk):
    if request.user.role != "security":
        return HttpResponseForbidden("Only security can edit visitors.")

    visitor = get_object_or_404(Visitor, pk=pk)

    if request.method == "POST":
        form = VisitorForm(request.POST, instance=visitor)
        formset = VisitorImageFormSet(request.POST, request.FILES, instance=visitor)

        if form.is_valid() and formset.is_valid():
            visitor = form.save(commit=False)

            if not visitor.address and visitor.resident:
                visitor.address = visitor.resident.address

            visitor.save()
            formset.save()

            return redirect("visitor_detail", pk=visitor.pk)
    else:
        form = VisitorForm(instance=visitor)
        formset = VisitorImageFormSet(instance=visitor)

    return render(request, "visitors/visitor_form.html", {
        "form": form,
        "formset": formset,
        "page_title": "Edit Visitor",
    })


@login_required
def visitor_delete(request, pk):
    if request.user.role != "security":
        return HttpResponseForbidden("Only security can delete visitors.")

    visitor = get_object_or_404(Visitor, pk=pk)

    if request.method == "POST":
        visitor.delete()
        return redirect("visitor_list")

    return render(request, "visitors/visitor_confirm_delete.html", {"visitor": visitor})