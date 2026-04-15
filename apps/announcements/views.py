from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden

from .models import Announcement
from .forms import AnnouncementForm


def is_juristic(user):
    return user.is_authenticated and user.role == "juristic"


@login_required
def announcement_list(request):
    announcements = Announcement.objects.select_related("created_by").all()
    return render(request, "announcements/announcement_list.html", {
        "announcements": announcements
    })


@login_required
def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    return render(request, "announcements/announcement_detail.html", {
        "announcement": announcement
    })


@login_required
def announcement_create(request):
    if not is_juristic(request.user):
        return HttpResponseForbidden("You do not have permission to create announcements.")

    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            return redirect("announcement_list")
    else:
        form = AnnouncementForm()

    return render(request, "announcements/announcement_form.html", {
        "form": form,
        "page_title": "Create Announcement"
    })


@login_required
def announcement_update(request, pk):
    if not is_juristic(request.user):
        return HttpResponseForbidden("You do not have permission to edit announcements.")

    announcement = get_object_or_404(Announcement, pk=pk)

    if request.method == "POST":
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect("announcement_detail", pk=announcement.pk)
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, "announcements/announcement_form.html", {
        "form": form,
        "page_title": "Edit Announcement"
    })


@login_required
def announcement_delete(request, pk):
    if not is_juristic(request.user):
        return HttpResponseForbidden("You do not have permission to delete announcements.")

    announcement = get_object_or_404(Announcement, pk=pk)

    if request.method == "POST":
        announcement.delete()
        return redirect("announcement_list")

    return render(request, "announcements/announcement_confirm_delete.html", {
        "announcement": announcement
    })