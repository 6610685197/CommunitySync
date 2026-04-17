from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.db.models import Sum
from decimal import Decimal

from apps.announcements.models import Announcement
from apps.visitors.models import Visitor
from apps.maintenance.models import MaintenanceRequest
from apps.payments.models import Bill
from apps.communities.models import FacilityBooking


@login_required
def resident_dashboard(request):
    if request.user.role != "resident":
        return HttpResponseForbidden("Only residents can access this dashboard.")

    user = request.user

    total_announcements = Announcement.objects.count()
    my_visitors_count = Visitor.objects.filter(resident=user).count()
    my_maintenance_count = MaintenanceRequest.objects.filter(resident=user).count()

    bills = Bill.objects.filter(resident=user)
    total_bill_amount = bills.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    unpaid_bill_amount = bills.filter(status__in=["unpaid", "rejected", "overdue"]).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    paid_bill_amount = bills.filter(status="paid").aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    pending_review_count = bills.filter(status="pending_review").count()

    recent_announcements = Announcement.objects.all()[:5]
    recent_visitors = Visitor.objects.filter(resident=user).order_by("-created_at")[:5]
    recent_maintenance = MaintenanceRequest.objects.filter(resident=user).order_by("-created_at")[:5]
    recent_bills = bills.order_by("-created_at")[:5]
    recent_bookings = FacilityBooking.objects.filter(resident=user).select_related(
        "facility_unit", "facility_unit__facility"
    ).order_by("-created_at")[:5]

    context = {
        "total_announcements": total_announcements,
        "my_visitors_count": my_visitors_count,
        "my_maintenance_count": my_maintenance_count,
        "total_bill_amount": total_bill_amount,
        "unpaid_bill_amount": unpaid_bill_amount,
        "paid_bill_amount": paid_bill_amount,
        "pending_review_count": pending_review_count,
        "recent_announcements": recent_announcements,
        "recent_visitors": recent_visitors,
        "recent_maintenance": recent_maintenance,
        "recent_bills": recent_bills,
        "recent_bookings": recent_bookings,
    }
    return render(request, "dashboard/resident_dashboard.html", context)