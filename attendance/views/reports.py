import datetime


from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

from attendance.models import Classroom, Student, School, Notes
from django.shortcuts import get_object_or_404, render, redirect

from attendance.utility import is_facilitator, getRedirectWithParam
from attendance.utility.reports import sendNotesReport, sendStudentsReport, generateNotesReport, generateStudentReport


@login_required
def reports(request):
    notes = Notes.objects.all()
    students = Student.objects.all()
    return render(request, 'attendance/reports.html', {
        'notes': notes,
        'student': students,
    })


@login_required
def report(request, report_type: str = 'notes'):
    '''
    Report selector. Need entity type, entity id, date range
    '''
    msg = request.GET.get('msg', None)
    if request.method != 'POST':
        return render(request, 'attendance/reportoptions.html', {
            'report_type': report_type,
            'message':msg
        })
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def sendReport(request, report_type: str = 'notes'):
    '''
    Send reports. Need entity type, entity id, date range
    '''
    if request.method != 'POST':
        return redirect('/reports')

    entity = request.POST.get('entity_type')
    try:
        start_date = datetime.datetime.strptime(request.POST.get('start', '--'), '%m/%d/%Y')
        end_date = datetime.datetime.strptime(request.POST.get('end', '--'), '%m/%d/%Y')
    except Exception as e:
        return getRedirectWithParam('Invalid dates', 'attendance:report', kwargs={'report_type':report_type})

    # flip them around if they start is after end
    if start_date > end_date:
        temp = start_date
        start_date = end_date
        end_date = temp

    if entity == 'school':
        entity_id = request.POST.get('school_id', None)
        if not entity_id:
            return getRedirectWithParam('Invalid School id', 'attendance:report', kwargs={'report_type':report_type})
        school = get_object_or_404(School, pk=entity_id)
        title = school.name
    elif entity == 'classroom':
        entity_id = request.POST.get('classroom_id', None)
        if not entity_id:
            return getRedirectWithParam('Invalid classroom id', 'attendance:report', kwargs={'report_type':report_type})
        classroom = get_object_or_404(Classroom, pk=entity_id)
        title = classroom
        school = classroom.school
    elif entity == 'student':
        entity_id = request.POST.get('student_id')
        if not entity_id:
            return getRedirectWithParam('Invalid student id', 'attendance:report', kwargs={'report_type':report_type})
        student = get_object_or_404(Student, pk=entity_id)
        school = student.classroom.school
        title = mark_safe(student.__str__() + ' <br/> ' + student.classroom.__str__())
    else:
        return render(request, 'attendance/sendreport.html', {'message': 'Invalid Entity Type'})

    message = ''
    show_all = is_facilitator(request.user) or request.user.is_superuser
    if report_type == 'notes':
        if (request.POST.get('sendreport', '') == '1'):
            email = request.POST.get('email')
            sendNotesReport(request.user, email, entity, entity_id, start_date, end_date, is_facilitator(request.user))
            message = "Notes report sent to {}".format(email)
        report = generateNotesReport(entity, entity_id, start_date, end_date, show_all, 'html')
    if report_type == 'students':
        if (request.POST.get('sendreport', '') == '1'):
            email = request.POST.get('email')
            sendStudentsReport(request.user, email, entity, entity_id, start_date, end_date)
            message = "Student report sent to {}".format(email)
        report = generateStudentReport(entity, entity_id, start_date, end_date, 'html')


    return render(request, 'attendance/sendreport.html', {
        'title': title,
        'report_type': report_type,
        'school': school,
        'start': start_date,
        'end': end_date,
        'entity_type': entity,
        'entity_id': entity_id,
        'message': message,
        'report': report
    })
