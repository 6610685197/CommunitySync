import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm,CustomUserCreationForm
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
from .adapters import DiscordAdapter, GoogleAdapter
from .utils import decode_jwt_without_verification
from .services import OAuthFacade
from django.utils import timezone
from datetime import datetime, time
from apps.visitors.models import Visitor
from apps.maintenance.models import MaintenanceRequest
from apps.payments.models import Bill
from apps.communities.models import FacilityBooking


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # Redirect based on Role [cite: 106, 109]
                if user.role == "juristic":
                    return redirect("admin_dashboard")
                elif user.role == "security":
                    return redirect("security_dashboard")
                elif user.role == "resident":
                    return redirect("resident_dashboard")
            else:
                return render(
                    request,
                    "accounts/login.html",
                    {"form": form, "error": "Invalid credentials"},
                )
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


# --- Destination Pages ---


@login_required
def admin_dashboard(request):
    # This corresponds to the "Dashboard" for Juristic Person [cite: 5]
    if request.user.role not in ["juristic", "security"]:
        return redirect("resident_dashboard")  # Prevent unauthorized access
        
    total_residents = CustomUser.objects.filter(role="resident").count()
    total_visitors = Visitor.objects.count()
    expected_visitors = Visitor.objects.filter(status="expected").count()
    arrived_visitors = Visitor.objects.filter(status="arrived").count()
    completed_visitors = Visitor.objects.filter(status="completed").count()
    total_maintenance = MaintenanceRequest.objects.count()
    total_bills = Bill.objects.count()
    
    context = {
        "total_residents": total_residents,
        "total_visitors": total_visitors,
        "expected_visitors": expected_visitors,
        "arrived_visitors": arrived_visitors,
        "completed_visitors": completed_visitors,
        "total_maintenance": total_maintenance,
        "total_bills": total_bills,
    }
        
    return render(request, "accounts/admin_dashboard.html", context)

@csrf_exempt
def oauth_auth(request):

    data = json.loads(request.body)
    token = data.get("access_token")
    provider = data.get("provider")

    facade = OAuthFacade()
    user = facade.authenticate(token, provider)

    login(request, user)

    return JsonResponse({"ok": True, "role": user.role})


def index(request):
    if request.user.is_authenticated:
        if request.user.role == "juristic":
            return redirect("admin_dashboard")
        elif request.user.role == "security":
            return redirect("security_dashboard")
        elif request.user.role == "resident":
            return redirect("resident_dashboard")

    return redirect("login")
    
@login_required
def create_account(request):
    # Only juristic can access this page
    if request.user.role != "juristic":
        return redirect("resident_dashboard")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_list")   # or user list page if you have one
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/create_account.html", {"form": form})

@login_required
def user_list(request):

    # Only juristic can access
    if request.user.role != "juristic":
        return redirect("resident_dashboard")

    users = CustomUser.objects.all().order_by("role", "username")

    context = {
        "users": users
    }

    return render(request, "accounts/user_list.html", context)

@login_required
def security_dashboard(request):
    if request.user.role not in ["security", "juristic"]:
        return redirect("login")

    today = timezone.localdate()

    visitors_today = Visitor.objects.filter(created_at__date=today).count()
    expected_count = Visitor.objects.filter(status="expected").count()
    arrived_count = Visitor.objects.filter(status="arrived").count()
    completed_count = Visitor.objects.filter(status="completed").count()

    recent_visitors = Visitor.objects.select_related("resident", "created_by").order_by("-created_at")[:10]

    context = {
        "visitors_today": visitors_today,
        "expected_count": expected_count,
        "arrived_count": arrived_count,
        "completed_count": completed_count,
        "recent_visitors": recent_visitors,
    }
    return render(request, "accounts/security_dashboard.html", context)


# --- Password Recovery ---

def forgot_password_view(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier")
        method = request.POST.get("method")

        try:
            user = CustomUser.objects.get(username=identifier)
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(email=identifier)
            except CustomUser.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect("forgot_password")
        
        request.session["reset_user_id"] = user.id

        if method == "email":
            if not user.email:
                messages.error(request, "User does not have an email address.")
                return redirect("forgot_password")
            
            # Generate 4 digit code
            code = str(random.randint(1000, 9999))
            request.session["reset_code"] = code
            
            # Send Email
            send_mail(
                "Password Reset Code",
                f"Your 4-digit password reset code is: {code}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, "We have sent a 4-digit code to your email.")
            return redirect("verify_otp")
            
        elif method == "plate":
            return redirect("verify_plate")
            
    return render(request, "accounts/forgot_password.html")

def verify_otp_view(request):
    if "reset_user_id" not in request.session or "reset_code" not in request.session:
        return redirect("forgot_password")
        
    if request.method == "POST":
        code1 = request.POST.get("code1", "")
        code2 = request.POST.get("code2", "")
        code3 = request.POST.get("code3", "")
        code4 = request.POST.get("code4", "")
        submitted_code = code1 + code2 + code3 + code4
        
        if submitted_code == request.session["reset_code"]:
            request.session["reset_verified"] = True
            return redirect("reset_password")
        else:
            messages.error(request, "Invalid or expired code.")
            
    return render(request, "accounts/verify_otp.html")

def verify_plate_view(request):
    if "reset_user_id" not in request.session:
        return redirect("forgot_password")
        
    if request.method == "POST":
        plate = request.POST.get("plate", "").strip()
        user_id = request.session["reset_user_id"]
        
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return redirect("forgot_password")
            
        if user.car_plate_num and user.car_plate_num.strip().lower() == plate.lower():
            request.session["reset_verified"] = True
            return redirect("reset_password")
        else:
            messages.error(request, "License plate does not match our records.")
            
    return render(request, "accounts/verify_plate.html")

def reset_password_view(request):
    if not request.session.get("reset_verified"):
        return redirect("forgot_password")
        
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        if password and password == confirm_password:
            user_id = request.session.get("reset_user_id")
            try:
                user = CustomUser.objects.get(id=user_id)
                user.set_password(password)
                user.save()
                messages.success(request, "Password successfully reset. You can now log in.")
                
                # clear session
                request.session.pop("reset_user_id", None)
                request.session.pop("reset_code", None)
                request.session.pop("reset_verified", None)
                
                return redirect("login")
            except CustomUser.DoesNotExist:
                pass
        else:
            messages.error(request, "Passwords do not match.")
            
    return render(request, "accounts/reset_password.html")