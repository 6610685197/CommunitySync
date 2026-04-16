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
        return redirect("resident_home")  # Prevent unauthorized access
    return render(request, "accounts/admin_dashboard.html")


@login_required
def resident_home(request):
    # This corresponds to the Mobile Web App for Residents
    if request.user.role != "resident":
        return redirect("admin_dashboard")
    return render(request, "accounts/resident_home.html")


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
    """A simple landing page that redirects based on authentication status."""
    if request.user.is_authenticated:
        if request.user.role == "juristic":
            return redirect("admin_dashboard")
        else:
            return redirect("resident_home")
    else:
        return redirect("login")
    
@login_required
def create_account(request):
    # Only juristic can access this page
    if request.user.role != "juristic":
        return redirect("resident_home")

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
        return redirect("resident_home")

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