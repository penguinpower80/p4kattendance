from django.shortcuts import render


def home(request):
    user = request.user
    return render(request, 'attendance/home.html')
