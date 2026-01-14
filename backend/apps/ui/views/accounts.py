from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def accounts(request):
    return render(request, "app/accounts/index.html")