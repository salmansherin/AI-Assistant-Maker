from django.shortcuts import render


def dashboard(request):
    return render(request, 'assistant/dashboard.html')
