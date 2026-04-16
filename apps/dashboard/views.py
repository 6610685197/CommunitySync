from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

from apps.announcements.models import Announcement
from apps.visitors.models import Visitor
from apps.maintenance.models import MaintenanceRequest


@login_required
def resident_dashboard(request):
    if request.user.role != "resident":
        return HttpResponseForbidden("Only residents can access this dashboard.")

    user = request.user

    total_announcements = Announcement.objects.count()

    my_visitors_count = Visitor.objects.filter(resident=user).count()
    expected_visitors_count = Visitor.objects.filter(resident=user, status="expected").count()
    arrived_visitors_count = Visitor.objects.filter(resident=user, status="arrived").count()

    my_maintenance_count = MaintenanceRequest.objects.filter(resident=user).count()
    pending_maintenance_count = MaintenanceRequest.objects.filter(
        resident=user,
        status="pending"
    ).count()
    completed_maintenance_count = MaintenanceRequest.objects.filter(
        resident=user,
        status="completed"
    ).count()

    recent_announcements = Announcement.objects.select_related("created_by").all()[:5]
    recent_visitors = Visitor.objects.filter(resident=user).order_by("-created_at")[:5]
    recent_maintenance = MaintenanceRequest.objects.filter(resident=user).order_by("-created_at")[:5]

    context = {
        "total_announcements": total_announcements,
        "my_visitors_count": my_visitors_count,
        "expected_visitors_count": expected_visitors_count,
        "arrived_visitors_count": arrived_visitors_count,
        "my_maintenance_count": my_maintenance_count,
        "pending_maintenance_count": pending_maintenance_count,
        "completed_maintenance_count": completed_maintenance_count,
        "recent_announcements": recent_announcements,
        "recent_visitors": recent_visitors,
        "recent_maintenance": recent_maintenance,
    }
    return render(request, "dashboard/resident_dashboard.html", context)