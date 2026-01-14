from django.urls import path

from apps.users.views.api import me, save_onboarding
from apps.users.views.onboarding import (
    entry, step1_intents, step2_goals, step3_profile, plaid_link
)
urlpatterns = [
    # App entry
    path("", entry, name="entry"),

    # API
    path("me", me, name="me"),
    path("onboarding/save", save_onboarding, name="save_onboarding"),

    # Onboarding pages
    path("onboarding/1/", step1_intents, name="onboarding_step1"),
    path("onboarding/2/", step2_goals, name="onboarding_step2"),
    path("onboarding/3/", step3_profile, name="onboarding_step3"),

    # Plaid
    path("plaid/link/", plaid_link, name="plaid_link"),
]
