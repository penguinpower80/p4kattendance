from django.shortcuts import redirect
from django.urls import reverse

from attendance.models import Assignments


def is_mentor(user):
    return user.groups.filter(name='Mentors').exists()

def is_facilitator(user):
    return user.groups.filter(name='Facilitators').exists()

def isAssigned(user, id, type):
    return Assignments.objects.filter(user=user).filter(tid=id).filter(type=type).count > 0

def assignmentsFor(user, type=None):
    if ( type ):
        return Assignments.objects.filter(user=user).filter(type=type).all()
    else:
        return Assignments.objects.filter(user=user).all()

def getRedirectWithParam(message, location='attendance:home'):
    base_url = reverse(location)
    url = '{}?msg={}'.format(base_url, message)
    return redirect(url)