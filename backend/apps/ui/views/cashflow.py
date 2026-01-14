from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def cashflow(request):
    return render(request, "app/cashflow/index.html")