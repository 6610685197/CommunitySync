from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser


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


@csrf_exempt
def discord_auth(request):
    """Receive Supabase access token and create/login a local user.
    
    The frontend sends the token from a successful Supabase session.
    We decode the JWT to extract user info (email, etc) without needing
    to make another API call to Supabase.
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
    except Exception as e:
        return JsonResponse({"error": f"invalid JSON: {str(e)}"}, status=400)

    token = data.get("access_token")
    if not token:
        return JsonResponse({"error": "access_token required"}, status=400)

    try:
        # Decode JWT parts without verification (we trust Supabase already verified it)
        # JWT format: header.payload.signature
        import base64
        parts = token.split(".")
        if len(parts) != 3:
            return JsonResponse({"error": "invalid token format"}, status=400)
        
        # Decode the payload (add padding if needed)
        payload_b64 = parts[1]
        padding = 4 - (len(payload_b64) % 4)
        if padding != 4:
            payload_b64 += "=" * padding
        
        payload_json = base64.urlsafe_b64decode(payload_b64)
        payload = json.loads(payload_json)
        
        # Extract email from the JWT payload
        email = payload.get("email")
        if not email:
            return JsonResponse({"error": "email not in token"}, status=400)
        
        # Extract user name from payload (Discord usually provides this)
        name = payload.get("name") or payload.get("email")
        
        # Find or create local user
        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                "username": email.split("@")[0],
                "name": name,
                "role": "resident",  # default role
            },
        )

        # Log the user in
        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user)

        return JsonResponse({"ok": True, "role": user.role})
    except Exception as e:
        return JsonResponse({"error": f"Token decode/processing error: {str(e)}"}, status=500)

def index(request):
    """A simple landing page that redirects based on authentication status."""
    if request.user.is_authenticated:
        if request.user.role == "juristic":
            return redirect("admin_dashboard")
        else:
            return redirect("resident_home")
    else:
        return redirect("login")