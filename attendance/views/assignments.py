import logging

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from attendance.models import School, Assignments, AssignmentTypes
from attendance.utility import is_facilitator, is_mentor, assignmentsFor, getRedirectWithParam

'''
TODO: Add some permissions checking!!
'''
def assignments(request):
    mentors = User.objects.filter(groups__name='Mentors')
    facilitators = User.objects.filter(groups__name='Facilitators')
    msg = request.GET.get('msg', None)
    return render(request, 'attendance/assignments.html', {
        'mentors': mentors,
        'facilitators': facilitators,
        'message': msg,
    })

'''
TODO: Add some permissions checking!!
'''
def assign(request, userid):
    targetuser = get_object_or_404(User, pk=userid)
    if request.method == 'POST':
        Assignments.objects.filter(user=targetuser).delete() #get rid of all old assignments
        schools = request.POST.getlist('school[]')
        mentors = request.POST.getlist('mentor[]')
        classes = request.POST.getlist('classroom[]')
        students = request.POST.getlist('student[]')
        for s in schools:
            Assignments(user=targetuser, type=AssignmentTypes.SCHOOL, tid=s).save()
        for s in mentors:
            Assignments(user=targetuser, type=AssignmentTypes.MENTOR, tid=s).save()
        for s in classes:
            Assignments(user=targetuser, type=AssignmentTypes.CLASSROOM, tid=s).save()
        for s in students:
            Assignments(user=targetuser, type=AssignmentTypes.STUDENT, tid=s).save()

        return getRedirectWithParam('Assignments Saved', 'attendance:assignments')

    assignments = assignmentsFor(targetuser)
    assignable = {}
    if is_facilitator(targetuser):
        assignable['mentors'] = User.objects.filter(groups__name='Mentors')
    assignable['schools'] = School.objects.all()
    return render(request, 'attendance/assign.html', {
        'assignments': assignments,
        'targetuser': targetuser,
        'assignable': assignable,
        'is_facilitator': is_facilitator(targetuser),
        'is_mentor': is_mentor(targetuser)
    })