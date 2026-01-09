# project/app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User

from .forms import ItemForm, EditProfileForm
from .models import LostItemReport


# ---------------- AUTH ----------------

def signup_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm_password']

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Account already exists")
            return redirect('signup')

        User.objects.create_user(username=email, password=password)
        messages.success(request, "Account created. Please login.")
        return redirect('login')

    return render(request, 'app/signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, "Invalid email or password")
        return redirect('login')

    return render(request, 'app/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# ---------------- DASHBOARD ----------------

@login_required
def dashboard(request):
    # SAVE ITEM FROM DASHBOARD
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.status = 'Pending'
            item.save()
            messages.success(request, "Item reported successfully")
            return redirect('dashboard')
    else:
        form = ItemForm()

    # LOAD TABLES
    pending_reports = LostItemReport.objects.filter(
        status='Pending'
    ).order_by('-date_reported')

    claimed_reports = LostItemReport.objects.filter(
        status='Claimed'
    ).order_by('-date_reported')

    return render(request, 'app/dashboard.html', {
        'form': form,
        'pending_reports': pending_reports,
        'claimed_reports': claimed_reports
    })


# ---------------- REPORT ITEM ----------------

@login_required
def report_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.status = 'Pending'
            item.save()
            messages.success(request, "Item reported successfully")
            return redirect('dashboard')
    else:
        form = ItemForm()

    return render(request, 'app/report.html', {'form': form})


# ---------------- CLAIM ----------------

@login_required
def claim_item(request, pk):
    item = get_object_or_404(LostItemReport, pk=pk)
    item.status = 'Claimed'
    item.save()
    messages.success(request, "Item marked as claimed")
    return redirect('dashboard')


# ---------------- PROFILE ----------------

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            updated = form.save(commit=False)
            password = form.cleaned_data.get('password')

            if password:
                updated.set_password(password)

            updated.save()

            if password:
                update_session_auth_hash(request, updated)

            messages.success(request, "Profile updated")
            return redirect('dashboard')
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'app/profile.html', {'form': form})

# views.py


# app/views.py

@login_required
def confirm_claim(request, pk):
    item = get_object_or_404(LostItemReport, pk=pk)

    if request.method == "POST":
        # Just mark as claimed directly
        item.status = "Claimed"
        item.save()
        messages.success(request, f"'{item.item_name}' successfully claimed!")
        return redirect("dashboard")  # Goes back to dashboard

    return render(request, "app/confirm_claim.html", {"item": item})
