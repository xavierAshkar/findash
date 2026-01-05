# apps/users/views/onboarding.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.users.models import UserProfile

@login_required
def entry(request):
    p, _ = UserProfile.objects.get_or_create(user=request.user)
    if p.onboarding_completed_at:
        return redirect("/app/dashboard/")
    return redirect("/app/onboarding/1/")


@login_required
def step1_intents(request):
    return render(request, "onboarding/step1_intents.html")

@login_required
def step2_goals(request):
    return render(request, "onboarding/step2_goals.html")



@login_required
def dashboard(request):
    return render(request, "onboarding/dashboard_placeholder.html")
