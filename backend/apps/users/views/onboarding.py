# apps/users/views/onboarding.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.users.models import UserProfile


def root(request):
    if request.user.is_authenticated:
        return redirect("/app/")
    return render(request, "core/root.html")

@login_required
def entry(request):
    p, _ = UserProfile.objects.get_or_create(user=request.user)
    if not p.step1_completed_at:
        return redirect("/app/onboarding/1/")
    if not p.step2_completed_at:
        return redirect("/app/onboarding/2/")
    if not p.step3_completed_at:
        return redirect("/app/onboarding/3/")
    if not p.plaid_linked_at:
        return redirect("/app/plaid/link/")
    return redirect("/app/dashboard/")

@login_required
def step1_intents(request):
    return render(request, "onboarding/step1_intents.html")

@login_required
def step2_goals(request):
    p, _ = UserProfile.objects.get_or_create(user=request.user)
    if not p.step1_completed_at:
        return redirect("/app/onboarding/1/")
    return render(request, "onboarding/step2_goals.html")

@login_required
def step3_profile(request):
    p, _ = UserProfile.objects.get_or_create(user=request.user)
    if not p.step2_completed_at:
        return redirect("/app/onboarding/2/")
    return render(request, "onboarding/step3_profile.html")

@login_required
def plaid_link(request):
    p, _ = UserProfile.objects.get_or_create(user=request.user)
    if not p.step3_completed_at:
        return redirect("/app/onboarding/3/")
    return render(request, "onboarding/plaid_link.html")

@login_required
def dashboard(request):
    p, _ = UserProfile.objects.get_or_create(user=request.user)
    if not p.onboarding_completed_at:
        return redirect("/app/")
    return render(request, "onboarding/dashboard_placeholder.html")
