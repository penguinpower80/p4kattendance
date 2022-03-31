import logging

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from attendance.models import Student, Meeting, Attendance
from attendance.utility import userAssignedToStudent


def markattendance(request, student_id, meeting_id):
    if not userAssignedToStudent(request.user, student_id):
        return HttpResponse(status=401)

    logging.warning(str(student_id))
    logging.warning(str(meeting_id))
    logging.critical(student_id)
    student = get_object_or_404(Student, pk=student_id)
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    status = request.POST.get("status", None)

    # remove any existing marks
    if (status == 'remove'):
        Attendance.objects.filter(user=request.user).filter(student=student).filter(meeting=meeting).delete()
        return HttpResponse(status=200)

    attendance_record = Attendance.objects.filter(user=request.user).filter(student=student).filter(meeting=meeting).all()[:1]

    if attendance_record:
        attendance_record[0].status = status
        attendance_record[0].save()
    else:
        Attendance.objects.create(
            user=request.user,
            student=student,
            meeting=meeting,
            status=status
        )

    return HttpResponse(status=200)
