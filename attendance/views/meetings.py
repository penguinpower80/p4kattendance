import datetime
import logging

from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from attendance.models import AssignmentTypes, Classroom, Student, Meeting, Attendance
from attendance.utility import isAssigned

'''
TODO: Add some permissions checking!!
'''


def meeting(request, type, id):
    if type == 'classroom':
        classroom = get_object_or_404(Classroom, pk=id)
        students = classroom.student_set.order_by('last_name','first_name').all()
        meeting_type = AssignmentTypes.CLASSROOM
        if not isAssigned(request.user, id, AssignmentTypes.CLASSROOM):
            raise PermissionDenied()

    if type == 'student':
        student = get_object_or_404(Student, pk=id)
        students = [student]
        classroom = student.classroom
        meeting_type = AssignmentTypes.STUDENT
        if not isAssigned(request.user, id, AssignmentTypes.STUDENT):
            raise PermissionDenied()


    preexisting = Meeting.objects.filter(user=request.user).filter(type=meeting_type).filter(tid='id').filter(date=datetime.datetime.now()).all()[:1]

    if preexisting:
        return redirect('/meeting/' + str(preexisting[0].id) )

    meeting = Meeting.objects.create(
        user=request.user,
        type=meeting_type,
        tid=id
    )


    return render(request, 'attendance/meeting.html', {
        'students': students,
        'classroom': classroom,
        'meeting': meeting,
        'attendance':None
    })


'''
  /meeting/edit/<id>
'''
def editmeeting(request, id):
    meeting = get_object_or_404(Meeting, pk=id)
    if meeting.type == AssignmentTypes.CLASSROOM:
        classroom = get_object_or_404(Classroom, pk=meeting.tid)
        students = classroom.student_set.order_by('last_name', 'first_name').all()

    if meeting.type == AssignmentTypes.STUDENT:
        student = get_object_or_404(Student, pk=meeting.tid)
        students = [student]
        classroom = student.classroom

    attendance = Attendance.objects.filter(meeting=meeting).all()

    return render(request, 'attendance/meeting.html', {
        'students': students,
        'classroom': classroom,
        'meeting': meeting,
        'attendance': attendance
    })
