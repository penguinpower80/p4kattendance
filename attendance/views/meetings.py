import datetime

from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404

from attendance.models import AssignmentTypes, Classroom, Student
from attendance.utility import isAssigned

'''
TODO: Add some permissions checking!!
'''


def meeting(request, type, id):
    if type == 'classroom':
        classroom = get_object_or_404(Classroom, pk=id)
        students = classroom.student_set.order_by('last_name','first_name').all()
        if not isAssigned(request.user, id, AssignmentTypes.CLASSROOM):
            raise PermissionDenied()

    if type == 'student':
        student = get_object_or_404(Student, pk=id)
        students = [student]
        classroom = student.classroom
        if not isAssigned(request.user, id, AssignmentTypes.STUDENT):
            raise PermissionDenied()

    return render(request, 'attendance/meeting.html', {
        'students': students,
        'classroom': classroom,
        'date': datetime.datetime.now()
    })


def editmeeting(request, id):
    pass
