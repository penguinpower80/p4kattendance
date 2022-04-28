import datetime
from os import path

from decouple import config
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from attendance.models import Assignments, Meeting, Attendance
from attendance.utility import isAssigned, is_mentor

register = template.Library()


@register.simple_tag(takes_context=True)
def logged_in_as(context):
    '''
    Return the user currently logged in.  Mostly for help in debugging.
    '''
    if context.request.user.is_anonymous:
        return ''
    return mark_safe('<div>Logged in as: {}</div>'.format(context.request.user.email))


@register.simple_tag()
def version():
    '''
    Shows the time stamp of last deployment, or "Local" to help with debugging
    '''
    last_deployed = ''
    try:
        this_host = config('HOSTING', default='LOCAL')
        if this_host == 'HEROKU':
            checkfile = path.join(settings.BASE_DIR, 'manage.py')
            if path.exists(checkfile):
                try:
                    with open(checkfile) as reader:
                        last_deployed = path.getctime(checkfile)
                        return datetime.datetime.fromtimestamp(last_deployed).strftime('%m/%d/%Y %H:%M:%S')
                except Exception as e:
                    last_deployed = '[unable to open file]'
            else:
                last_deployed = '[check file not found]'
        else:
            last_deployed = 'Environment: ' + this_host
    except AttributeError as e:
        last_deployed = '[HOSTING not set in .env]'
    return last_deployed


@register.simple_tag(takes_context=True)
def current_view_class(context):
    '''
    Returns some classes that help apply context specific styling to the site.
    '''
    classes = []
    if context.request.user.is_anonymous:
        classes.append("user-anonymous")
    if context.request.user.is_superuser:
        classes.append("user-sysadmin")

    if context.request.path == '/':
        classes.append("page-home")
    else:
        classes.append('page-' + context.request.path[1:].replace('/', '-'))

    return " ".join(classes)


@register.simple_tag()
def status_class(status):
    '''
    Converts a status class to bulma.io class.
    '''
    if status == 'error':
        return 'is-danger'
    if status == 'success':
        return 'is-success'
    if status == 'warning':
        return 'is-warning'
    return 'is-info'


@register.filter(name='getkey')
def getkey(value, arg):
    '''
    https://stackoverflow.com/questions/1906129/dict-keys-with-spaces-in-django-templates
    Get a value from a dictionary with key that has a space
    '''
    return value[arg]


@register.simple_tag()
def assigned_to(type, id, text="<li>No one</li>"):
    '''
    Return assignments for a student.  Was used for one version of the student report, but not the final implemented version
    '''
    try:
        assignments = Assignments.objects.filter(type=type, tid=id).all()
    except Assignments.DoesNotExist as e:
        return mark_safe(text)

    if assignments.count() == 0:
        return mark_safe(text)

    user_list = ''
    for assignment in assignments:
        user_list += "<li>{} ({})</li>".format(assignment.user.get_full_name(), 'Mentor' if is_mentor(assignment.user) else 'Facilitator')

    return mark_safe(user_list)


@register.simple_tag()
def isassigned(type, id, assignments, text="None"):
    '''
    Returns specific text if type and id show up in the assignments list
    '''
    if assignments.filter(type=type, tid=id).count() > 0:
        return text
    else:
        return ""


@register.simple_tag()
def has_attendance_of(set, student, type, text=' is-primary'):
    '''
    Returns some text (mostly for styling) if the student has the specified attendance record
    '''
    if set is not None:
        result = set.filter(student_id=student)
        if result.count() > 0:
            if result[0].status == type:
                return text
    return ''



@register.filter(name='has_group')
def has_group(user, group_name):
    '''
        https://stackoverflow.com/questions/34571880/how-to-check-in-template-if-user-belongs-to-a-group
        returns true if the user belongs to a specific group
    '''
    return user.groups.filter(name=group_name).exists()


@register.simple_tag()
def attendance_date(date):
    '''
    Returns a formatted date
    '''
    if date is None:
        return ''
    try:
        this_date = date.strftime('%m/%d/%Y')
        return this_date
    except AttributeError:
        return '-'


@register.simple_tag()
def attendance(id, start, end):
    '''
    Returns the attendance dates and status for a given time period
    '''
    delta = datetime.timedelta(days=1)
    str = ''

    meetings = Meeting.objects.filter(date__range=(start, end), type='P').all()
    if meetings.count() == 0:
        return mark_safe('<li>No meetings recorded.</li>')
    attendances = Attendance.objects.filter(student_id=id, meeting_id__in=meetings)
    if attendances.count() == 0:
        return mark_safe('<li>No attendance recorded.</li>')
    for attendance in attendances:
        str += "<li>" + attendance.meeting.date.strftime('%m/%d/%Y') + " - " + attendance.get_status_display() + "</li>"
    return mark_safe(str)
