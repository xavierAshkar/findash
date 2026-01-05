# apps/users/views/api.py

import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from apps.users.models import UserProfile


@login_required
@require_http_methods(["GET"])
def me(request):
    p, _ = UserProfile.objects.get_or_create(user=request.user)
    return JsonResponse(
        {
            "user": {"id": request.user.id, "email": getattr(request.user, "email", "")},
            "profile": {
                "product_intents": p.product_intents,
                "financial_goals": p.financial_goals,
                "has_student_loans": p.has_student_loans,
                "has_credit_card_debt": p.has_credit_card_debt,
                "has_car_payments": p.has_car_payments,
                "housing_status": p.housing_status,
                "onboarding_completed_at": p.onboarding_completed_at.isoformat() if p.onboarding_completed_at else None,
            },
        }
    )


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def save_onboarding(request):
    data = json.loads(request.body.decode("utf-8")) if request.body else {}
    p, _ = UserProfile.objects.get_or_create(user=request.user)

    if "product_intents" in data:
        p.product_intents = data["product_intents"]
    if "financial_goals" in data:
        p.financial_goals = data["financial_goals"]

    if "obligations" in data:
        flags = set(data["obligations"])
        p.has_student_loans = "STUDENT_LOANS" in flags
        p.has_credit_card_debt = "CREDIT_CARD_DEBT" in flags
        p.has_car_payments = "CAR_PAYMENTS" in flags

        if "OWN" in flags:
            p.housing_status = "OWN"
        elif "RENT" in flags:
            p.housing_status = "RENT"

    if data.get("complete") is True:
        p.onboarding_completed_at = timezone.now()

    p.save()
    return JsonResponse({"ok": True})