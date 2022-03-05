import logging

from django.shortcuts import render

from attendance.models import School


def assigntest(request):
    schools = School.objects.all()
    logging.warning(schools)
    return render(request, 'attendance/assignment_test.html',{
        'schools': schools
    })
