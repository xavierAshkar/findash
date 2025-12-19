from django.shortcuts import render

def plaid_test(request):
    return render(request, "plaid_link/plaid_test.html")

