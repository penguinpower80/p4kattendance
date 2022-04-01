import logging

from django.shortcuts import render

from attendance.models import School


def assigntest(request):
    schools = School.objects.all()
    return render(request, 'attendance/assignment_test.html',{
        'schools': schools
    })
