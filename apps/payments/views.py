from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.accounts.models import CustomUser
from .models import BillingRule, BillingRuleResident, Bill, PaymentReceipt
from .forms import BillingRuleForm, BillForm, PaymentReceiptForm, PaymentReceiptReviewForm


def is_juristic(user):
    return user.is_authenticated and user.role == "juristic"


def is_resident(user):
    return user.is_authenticated and user.role == "resident"


@login_required
def bill_list(request):
    Bill.objects.filter(
        status="unpaid",
        due_date__lt=timezone.localdate()
    ).update(status="overdue")

    if is_juristic(request.user):
        bills = Bill.objects.select_related("resident", "billing_rule").all()
    elif is_resident(request.user):
        bills = Bill.objects.select_related("resident", "billing_rule").filter(resident=request.user)
    else:
        return HttpResponseForbidden("No permission.")

    return render(request, "payments/bill_list.html", {"bills": bills})


@login_required
def bill_detail(request, pk):
    Bill.objects.filter(
        status="unpaid",
        due_date__lt=timezone.localdate()
    ).update(status="overdue")

    bill = get_object_or_404(
        Bill.objects.select_related("resident", "billing_rule", "created_by"),
        pk=pk,
    )

    if is_resident(request.user) and bill.resident != request.user:
        return HttpResponseForbidden("No permission.")

    if request.user.role not in ["resident", "juristic"]:
        return HttpResponseForbidden("No permission.")

    receipt_form = None
    if is_resident(request.user) and bill.resident == request.user:
        receipt_form = PaymentReceiptForm()

    return render(request, "payments/bill_detail.html", {
        "bill": bill,
        "receipt_form": receipt_form,
    })


@login_required
def bill_create(request):
    if not is_juristic(request.user):
        return HttpResponseForbidden("Only juristic can create bills.")

    if request.method == "POST":
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.created_by = request.user
            bill.save()
            messages.success(request, "Bill created successfully.")
            return redirect("bill_list")
    else:
        form = BillForm()

    return render(request, "payments/bill_form.html", {
        "form": form,
        "page_title": "Create Bill",
    })


@login_required
def bill_update(request, pk):
    if not is_juristic(request.user):
        return HttpResponseForbidden("Only juristic can edit bills.")

    bill = get_object_or_404(Bill, pk=pk)

    if request.method == "POST":
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            messages.success(request, "Bill updated successfully.")
            return redirect("bill_detail", pk=bill.pk)
    else:
        form = BillForm(instance=bill)

    return render(request, "payments/bill_form.html", {
        "form": form,
        "page_title": "Edit Bill",
    })


@login_required
def bill_delete(request, pk):
    if not is_juristic(request.user):
        return HttpResponseForbidden("Only juristic can delete bills.")

    bill = get_object_or_404(Bill, pk=pk)

    if request.method == "POST":
        bill.delete()
        messages.success(request, "Bill deleted successfully.")
        return redirect("bill_list")

    return render(request, "payments/bill_confirm_delete.html", {"bill": bill})


@login_required
def upload_receipt(request, pk):
    bill = get_object_or_404(Bill, pk=pk)

    if not is_resident(request.user) or bill.resident != request.user:
        return HttpResponseForbidden("Only the bill owner can upload receipt.")

    if request.method == "POST":
        form = PaymentReceiptForm(request.POST, request.FILES)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.bill = bill
            receipt.submitted_by = request.user
            receipt.save()

            bill.status = "pending_review"
            bill.save()

            messages.success(request, "Receipt submitted successfully.")
            return redirect("bill_detail", pk=bill.pk)

    return redirect("bill_detail", pk=bill.pk)


@login_required
def review_receipt(request, receipt_id):
    if not is_juristic(request.user):
        return HttpResponseForbidden("Only juristic can review receipts.")

    receipt = get_object_or_404(PaymentReceipt.objects.select_related("bill"), pk=receipt_id)

    if request.method == "POST":
        form = PaymentReceiptReviewForm(request.POST, instance=receipt)
        if form.is_valid():
            reviewed_receipt = form.save(commit=False)
            reviewed_receipt.reviewed_by = request.user
            reviewed_receipt.reviewed_at = timezone.now()
            reviewed_receipt.save()

            bill = receipt.bill
            if reviewed_receipt.status == "approved":
                bill.status = "paid"
            elif reviewed_receipt.status == "rejected":
                bill.status = "rejected"
            else:
                bill.status = "pending_review"
            bill.save()

            messages.success(request, "Receipt reviewed successfully.")
            return redirect("bill_detail", pk=bill.pk)
    else:
        form = PaymentReceiptReviewForm(instance=receipt)

    return render(request, "payments/review_receipt.html", {
        "receipt": receipt,
        "form": form,
    })


@login_required
def billing_rule_list(request):
    if not is_juristic(request.user):
        return HttpResponseForbidden("Only juristic can manage billing rules.")

    rules = BillingRule.objects.all()
    return render(request, "payments/billing_rule_list.html", {"rules": rules})


@login_required
def billing_rule_create(request):
    if not is_juristic(request.user):
        return HttpResponseForbidden("Only juristic can create billing rules.")

    if request.method == "POST":
        form = BillingRuleForm(request.POST)
        if form.is_valid():
            rule = form.save()
            if rule.target_type == "selected":
                resident_ids = request.POST.getlist("resident_ids")
                for resident_id in resident_ids:
                    try:
                        resident = CustomUser.objects.get(id=resident_id, role="resident")
                        BillingRuleResident.objects.get_or_create(rule=rule, resident=resident)
                    except CustomUser.DoesNotExist:
                        pass

            messages.success(request, "Billing rule created successfully.")
            return redirect("billing_rule_list")
    else:
        form = BillingRuleForm()

    residents = CustomUser.objects.filter(role="resident").order_by("username")
    return render(request, "payments/billing_rule_form.html", {
        "form": form,
        "page_title": "Create Billing Rule",
        "residents": residents,
    })


@login_required
def generate_bills_from_rule(request, rule_id):
    if not is_juristic(request.user):
        return HttpResponseForbidden("Only juristic can generate bills.")

    rule = get_object_or_404(BillingRule, pk=rule_id)

    if request.method == "POST":
        month = request.POST.get("billing_month")
        year = request.POST.get("billing_year")
        due_date = request.POST.get("due_date")

        if not due_date:
            messages.error(request, "Due date is required.")
            return redirect("billing_rule_list")

        if rule.target_type == "all":
            residents = CustomUser.objects.filter(role="resident")
        else:
            residents = CustomUser.objects.filter(
                id__in=rule.rule_residents.values_list("resident_id", flat=True),
                role="resident"
            )

        created_count = 0
        for resident in residents:
            if month and year:
                exists = Bill.objects.filter(
                    resident=resident,
                    billing_rule=rule,
                    billing_month=month,
                    billing_year=year,
                ).exists()
                if exists:
                    continue

            Bill.objects.create(
                resident=resident,
                name=rule.name,
                billing_rule=rule,
                title=f"{rule.name} Bill",
                description=f"Generated from rule: {rule.name}",
                amount=rule.default_amount or 0,
                due_date=due_date,
                billing_month=month or None,
                billing_year=year or None,
                status="unpaid",
                created_by=request.user,
            )
            created_count += 1

        messages.success(request, f"Generated {created_count} bill(s).")
        return redirect("bill_list")

    return redirect("billing_rule_list")