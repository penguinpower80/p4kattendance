import datetime
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from attendance.models import Student, Meeting, Attendance, Classroom, AssignmentTypes
from attendance.utility import userAssignedToStudent, meetingsFor


@login_required
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

@login_required
def meetinglist(request, entity, entity_id):
    if entity == AssignmentTypes.CLASSROOM:
        classroom = get_object_or_404(Classroom, pk=entity_id)
    if entity == AssignmentTypes.STUDENT:
        student = get_object_or_404(Student, pk=entity_id)
        classroom = student.classroom

    meetings = meetingsFor(request.user, entity, entity_id, True)
    if meetings is None:
        return JsonResponse({})
    return JsonResponse( meetings, safe=False)

def setmeetingdate(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    timestamp = request.POST.get("timestamp", None)

    if timestamp is not None:
        print(timestamp)
        newdate = datetime.datetime.strptime(timestamp, '%m/%d/%Y')
        meeting.date = newdate
        meeting.save()
        return HttpResponse(meeting.date.strftime('%m/%d/%Y'), status=200)

    return HttpResponse(status=500)
