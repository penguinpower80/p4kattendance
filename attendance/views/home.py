from django.shortcuts import render


def home(request):
    user = request.user
    if user.is_anonymous:
        return render(request, 'attendance/home.html')
