from django.shortcuts import render
from django.views.generic import ListView
from attendance.models import Student


class ReportListView(ListView):
    model = Student
    template_name = 'attendance/reports.html'

