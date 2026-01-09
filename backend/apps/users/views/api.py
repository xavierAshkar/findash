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
                "pays_rent": p.pays_rent,
                "has_mortgage": p.has_mortgage,
                "step1_completed_at": p.step1_completed_at.isoformat() if p.step1_completed_at else None,
                "step2_completed_at": p.step2_completed_at.isoformat() if p.step2_completed_at else None,
                "step3_completed_at": p.step3_completed_at.isoformat() if p.step3_completed_at else None,
                "plaid_linked_at": p.plaid_linked_at.isoformat() if p.plaid_linked_at else None,
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
    now = timezone.now()

    if "product_intents" in data:
        intents = data["product_intents"]
        if not isinstance(intents, list):
            return JsonResponse({"ok": False, "error": "invalid_product_intents"}, status=400)
        p.product_intents = intents
        if not p.step1_completed_at:
            p.step1_completed_at = now


    if "financial_goals" in data:
        goals = data["financial_goals"]
        if not isinstance(goals, list) or len(goals) == 0:
            return JsonResponse({"ok": False, "error": "financial_goals_required"}, status=400)
        p.financial_goals = goals
        if not p.step2_completed_at:
            p.step2_completed_at = now

    STEP3_FIELDS = [
        "has_student_loans",
        "has_credit_card_debt",
        "has_car_payments",
        "pays_rent",
        "has_mortgage",
    ]

    if any(field in data for field in STEP3_FIELDS):
        for field in STEP3_FIELDS:
            if field in data:
                setattr(p, field, bool(data[field]))

        if not p.step3_completed_at:
            p.step3_completed_at = now



    p.save()
    return JsonResponse({"ok": True})