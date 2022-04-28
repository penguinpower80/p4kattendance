from datetime import datetime
from django.core.mail import EmailMessage
import weasyprint
from decouple import config

from attendance.models import School, Classroom, Student, AssignmentTypes, Notes
from django.template.loader import render_to_string


def generateNotesReport(entity, entity_id, start_date, end_date, show_all, view='pdf'):
    if entity == 'school':
        school = School.objects.get(pk=entity_id)
        classroom = None
        student = None
        type = AssignmentTypes.SCHOOL
        title = school.name.title()
        subtitle = ''
    elif entity == 'classroom':
        classroom = Classroom.objects.get(pk=entity_id)
        school = classroom.school
        type = AssignmentTypes.CLASSROOM
        student = None
        title = classroom
        subtitle = school.name.title()
    elif entity == 'student':
        type = AssignmentTypes.STUDENT
        student = Student.objects.get(pk=entity_id)
        classroom = student.classroom
        school = classroom.school
        title = student
        subtitle = school.name.title() + ', ' + classroom.name

    else:
        raise Exception('Invalid report entity.')

    try:
        notes = Notes.objects.filter(type=type, tid=entity_id,created_at__range=(start_date, end_date)).order_by('-created_at').all()
        if not show_all:
            notes = notes.filter(visible=True)
    except Notes.DoesNotExist as e:
        notes = None

    if view == 'pdf':
        template = 'reports/notes_pdf.html'
    else:
        template = 'reports/notes_html.html'
    return render_to_string(template, {
        'student': student,
        'school': school,
        'classroom': classroom,
        'notes': notes,
        'start': start_date,
        'end': end_date,
        'title': title,
        'subtitle': subtitle
    })

def generateStudentReport(entity, entity_id,start_date, end_date, view='pdf'):
    student = None
    if entity == 'school':
        school = School.objects.get(pk=entity_id)
        classrooms = Classroom.objects.filter(school_id=entity_id).all()
        title = school.name.title()
    elif entity == 'classroom':
        # just one, but still want it as a set for simple template
        classrooms = Classroom.objects.filter(pk=entity_id).all()
        title = classrooms[0].school.name.title()
    else:
        student = Student.objects.filter(pk=entity_id).get()
        classrooms = [student.classroom]
        title = student.__str__()

    if view == 'pdf':
        template = 'reports/students_pdf.html'
    else:
        template = 'reports/students_html.html'

    return render_to_string(template, {
        'classrooms': classrooms,
        'type': entity,
        'title': title,
        'start_date': start_date,
        'end_date': end_date,
        'student': student
    })



def sendNotesReport(sender, to, entity, entity_id, start_date, end_date, show_all=True, ):
    '''
    Send a notes report as an attachment in email. Entity can be a school, classroom, student,or user
    '''
    subject = "Notes Report for P4K"
    message = "Please find attached a {} report from the Partnership 4 Kids system.  " \
              "This report was generated by {} on {}".format(entity, sender, datetime.now())
    report = generateNotesReport(entity, entity_id, start_date, end_date, show_all)

    email = EmailMessage(
        subject,
        message,
        config('FROM', default=None),
        [to]
    )

    pdf = weasyprint.HTML(string=report).write_pdf()
    email.attach(f'{entity}_{entity_id}_notes_report.pdf', pdf, 'application/pdf')
    email.send(fail_silently=False)

def sendStudentsReport(sender, to, entity, entity_id, start_date, end_date):
    '''
    Send a student list in email.  Entity can be a school, classroom, user
    '''
    subject = "Students Report for P4K"
    message = "Please find attached a {} report of student assignments from the Partnership 4 Kids system.  " \
              "This report was generated by {} on {}".format(entity, sender, datetime.now())
    report = generateStudentReport(entity, entity_id, start_date, end_date)

    email = EmailMessage(
        subject,
        message,
        config('FROM', default=None),
        [to]
    )

    pdf = weasyprint.HTML(string=report).write_pdf()
    email.attach(f'{entity}_{entity_id}_students_report.pdf', pdf, 'application/pdf')
    email.send(fail_silently=False)
