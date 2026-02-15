from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


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
                elif user.role == "resident":
                    return redirect("resident_home")
                else:
                    return redirect("resident_home")  # Default fallback
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
    if request.user.role != "juristic":
        return redirect("resident_home")  # Prevent unauthorized access
    return render(request, "accounts/admin_dashboard.html")


@login_required
def resident_home(request):
    # This corresponds to the Mobile Web App for Residents
    if request.user.role != "resident":
        return redirect("admin_dashboard")
    return render(request, "accounts/resident_home.html")
