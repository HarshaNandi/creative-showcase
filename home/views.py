from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Image
import random

# Landing
def landing(request):
    images = list(Image.objects.all())
    random.shuffle(images)
    return render(request, "landing.html", {"images": images[:30]})


# Signup
def signupPage(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


# Login
def loginPage(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logoutUser(request):
    logout(request)
    return redirect("landing")


# Dashboard
@login_required
def dashboard(request):
    images = Image.objects.filter(user=request.user)
    return render(request, "dashboard.html", {"images": images})


# Upload
@login_required
def uploadImage(request):
    if request.method == "POST":
        img = request.FILES["image"]
        Image.objects.create(user=request.user, image=img)
    return redirect("dashboard")


# Public Profile
def publicProfile(request, username):
    user = User.objects.get(username=username)
    images = Image.objects.filter(user=user)
    return render(request, "profile.html", {"images": images, "userProfile": user})
@login_required
def uploadImage(request):
    if request.method == "POST":
        image_file = request.FILES.get("image")

        if image_file:
            Image.objects.create(
                user=request.user,
                image=image_file
            )

    return redirect("dashboard")


from django.contrib.auth.decorators import login_required

@login_required

def dashboard(request):
    today = datetime.date.today()

    # Record today's activity
    DailyActivity.objects.get_or_create(user=request.user, date=today)

    # Fetch all user active dates
    days = DailyActivity.objects.filter(user=request.user).values_list("date", flat=True)

    # ---------- STREAK ----------
    streak = 0
    d = today
    while d in days:
        streak += 1
        d -= datetime.timedelta(days=1)

    # ---------- CALENDAR ----------
    year = today.year
    month = today.month

    month_calendar = calendar.monthcalendar(year, month)

    # Prepare list of active days in this month (as numbers)
    active_days = [d.day for d in days if d.month == month and d.year == year]

    context = {
        "images": Image.objects.filter(user=request.user),
        "streak": streak,
        "month_calendar": month_calendar,
        "year": year,
        "month_name": calendar.month_name[month],
        "active_days": active_days,   # <-- clean & simple
    }

    return render(request, "dashboard.html", context)


import datetime
import calendar
from .models import DailyActivity
