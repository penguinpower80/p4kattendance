from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView
from attendance.models import Student


@login_required
class ReportListView(ListView):
    model = Student
    template_name = 'attendance/reports.html'

