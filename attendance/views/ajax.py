import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from attendance.models import Student, Meeting, Attendance, Classroom, AssignmentTypes, Notes, School
from attendance.utility import userAssignedToStudent, meetingsFor

'''
Handles marking attendance
'''


@login_required
def markattendance(request, student_id, meeting_id):
    if not userAssignedToStudent(request.user, student_id):
        return HttpResponse(status=401)

    student = get_object_or_404(Student, pk=student_id)
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    status = request.POST.get("status", None)

    # remove any existing marks
    if (status == 'remove'):
        Attendance.objects.filter(user=request.user).filter(student=student).filter(meeting=meeting).delete()
        return HttpResponse(status=200)

    attendance_record = Attendance.objects.filter(user=request.user).filter(student=student).filter(
        meeting=meeting).all()[:1]

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


'''
Handles meeting list
'''


@login_required()
def noteslist(request, entity, entity_id):
    if entity == 'classroom':
        entity_type = AssignmentTypes.CLASSROOM
    if entity == 'school':
        entity_type = AssignmentTypes.SCHOOL
    if entity == 'student':
        entity_type = AssignmentTypes.STUDENT

    notes = Notes.objects.filter(type=entity_type, tid=entity_id).order_by('-created_at')
    if not request.user.groups.filter(name='Facilitators').exists():
        notes = notes.filter(visible=True)
        is_facilitator = False
    else:
        is_facilitator = True

    if notes.count() == 0:
        return JsonResponse({'msg': "No notes found"})

    time_format = '%m/%d/%Y %-I:%M %P'
    notes_list = [{
        'id': note.pk,
        'author': note.author.get_full_name(),
        'author_id': note.author_id,
        'can_modify': (request.user == note.author or is_facilitator),
        'text': note.text,
        'created': note.created_at.strftime(time_format),
        'updated': note.updated_at.strftime(time_format)
    } for note in notes]

    response = {
        'msg': '{} note(s) retrieved.'.format(notes.count()),
        'notes': notes_list
    }

    return JsonResponse(response, safe=False)


@login_required
def meetinglist(request, entity, entity_id):
    '''
    Handles getting a meeting list
    '''
    if entity == AssignmentTypes.CLASSROOM:
        classroom = get_object_or_404(Classroom, pk=entity_id)
    if entity == AssignmentTypes.STUDENT:
        student = get_object_or_404(Student, pk=entity_id)
        classroom = student.classroom

    meetings = meetingsFor(request.user, entity, entity_id, True)

    if meetings is None:
        return JsonResponse({})

    for meeting in meetings:
        meeting['formatted'] = meeting['date'].strftime('%b %-d, %Y')

    return JsonResponse(meetings, safe=False)


@login_required
def setmeetingdate(request, meeting_id):
    '''
    Hanldes updating the date for a meeting
    '''
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    timestamp = request.POST.get("timestamp", None)

    if timestamp is not None:
        newdate = datetime.datetime.strptime(timestamp, '%m/%d/%Y')
        meeting.date = newdate
        meeting.save()
        return HttpResponse(meeting.date.strftime('%m/%d/%Y'), status=200)

    return HttpResponse(status=500)


@login_required()
def savenote(request, entity, entity_id):
    '''
    Handles saving a note
    '''
    if entity == 'classroom':
        entity_object = get_object_or_404(Classroom, pk=entity_id)
        meeting_type = AssignmentTypes.CLASSROOM
    if entity == 'student':
        entity_object = get_object_or_404(Student, pk=entity_id)
        meeting_type = AssignmentTypes.STUDENT
    if entity == 'school':
        entity_object = get_object_or_404(School, pk=entity_id)
        meeting_type = AssignmentTypes.SCHOOL

    text = request.POST.get("text", None)

    visible = request.POST.get("visible", 'true') == 'true'
    if text is None or text == '':
        return HttpResponse('You must provide text!', status=500)

    note = Notes.objects.create(
        author=request.user,
        type=meeting_type,
        tid=entity_id,
        text=text,
        visible=visible
    )

    return HttpResponse(status=200)


@login_required()
def updatenote(request, note_id):
    '''
    Handles updating a note
    '''

    note_object = get_object_or_404(Notes, pk=note_id)
    text = request.POST.get("text", None)
    visible = request.POST.get("visible", 'true') == 'true'
    if text is None or text == '':
        return HttpResponse('You must provide text!', status=500)

    note_object.text = text
    note_object.visible = visible
    note_object.save()

    return HttpResponse(status=200)


@login_required()
def deletenote(request, id):
    '''
    handle delete note
    '''
    note = get_object_or_404(Notes, pk=id)
    if note.author == request.user or request.user.groups.filter(name='Facilitators').exists():
        note.delete();
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=401)
