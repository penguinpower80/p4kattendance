from django.contrib.auth.decorators import login_required
django.shortcuts import render
from django.views.generic import ListView
from attendance.models import Student

@login_required
def reports(request):
    context = {}
    return render(request, 'attendance/reports.html', context=context)

