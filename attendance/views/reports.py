import datetime

from django.contrib.auth.decorators import login_required

from attendance.models import AssignmentTypes, Classroom, Student, School, Notes
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.dateparse import parse_datetime, parse_date

from attendance.utility import is_facilitator, is_mentor
from attendance.utility.reports import sendNotesReport, sendStudentsReport

@login_required
def reports(request):
    notes = Notes.objects.all()
    students = Student.objects.all()
    return render(request, 'attendance/reports.html', {
        'notes': notes,
        'student': students,
    })


@login_required
def report(request, report_type:str = 'notes'):
    '''
    Report selector. Need entity type, entity id, date range
    '''
    if request.method != 'POST':
        if report_type == 'notes':
            return render(request, 'reports/notesreportoptions.html')
        if report_type == 'students':
            return render(request, 'reports/studentsreportoptions.html')
        return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def sendReport(request, report_type:str = 'notes'):
    '''
    Send reports. Need entity type, entity id, date range
    '''
    if request.method != 'POST':
        return render(request, 'attendance/sendreporttest.html')
        return redirect(request.META.get('HTTP_REFERER', '/'))


    entity = request.POST.get('entity_type')
    entity_id = request.POST.get('entity_id')
    try:
        start_date = datetime.datetime.strptime( request.POST.get('start', ''), '%m/%d/%Y' )
        end_date = datetime.datetime.strptime( request.POST.get('end', ''), '%m/%d/%Y' )
    except Exception as e:
        return render(request, 'attendance/sendreporttest.html', {'message': 'Invalid Date'})

    # flip them around if they start is after end
    if start_date > end_date:
        temp = start_date
        start_date = end_date
        end_date = temp



    if entity == 'school':
        school = get_object_or_404(School, pk=entity_id)
    elif entity == 'classroom':
        classroom = get_object_or_404(Classroom, pk=entity_id)
        school = classroom.school
    elif entity == 'student':
        student = get_object_or_404(Student, pk=entity_id)
        school = student.classroom.school
    else:
        return render(request, 'attendance/sendreporttest.html', {'message': 'Invalid Entity Type'})

    message=''

    if ( request.POST.get('sendreport', '') == '1'):
        print( 'need to send' )
        email = request.POST.get('email')
        if report_type == 'notes':
            sendNotesReport(request.user, email, entity, entity_id, start_date, end_date, is_facilitator(request.user) )
            message = "Notes report sent to {}".format(email)
        if report_type == 'students':
            sendStudentsReport(request.user, email, entity, entity_id)
            message = "Student report sent to {}".format(email)


    return render(request, 'attendance/sendreport.html', {
        'report_type': report_type,
        'school': school,
        'start': start_date,
        'end': end_date,
        'entity_type': entity,
        'entity_id': entity_id,
        'message': message
    })
