import logging

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from attendance.models import School, Assignments, AssignmentTypes
from attendance.utility import is_facilitator, is_mentor, assignmentsFor, getRedirectWithParam

'''
TODO: Add some permissions checking!!
'''
@user_passes_test(lambda u: u.is_superuser or is_facilitator)
def assignments(request):
    if request.user.is_superuser:
        facilitators = User.objects.filter(groups__name='Facilitators')
        mentors = User.objects.filter(groups__name='Mentors')
    else:
        facilitators = False
        myMentors = Assignments.objects.filter(type=AssignmentTypes.MENTOR, user=request.user).values_list('tid', flat=True)
        if myMentors.count() > 0:
            mentors = User.objects.filter(groups__name='Mentors', id__in=myMentors).all()
        else:
            mentors = User.objects.filter(groups__name='Mentors')

    msg = request.GET.get('msg', None)
    return render(request, 'attendance/assignments.html', {
        'mentors': mentors,
        'facilitators': facilitators,
        'message': msg,
    })

'''
TODO: Add some permissions checking!!
'''
@user_passes_test(lambda u: u.is_superuser or is_facilitator)
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

    if request.user.is_superuser:
        assignable['schools'] = School.objects.all()
    else:
        mySchools = Assignments.objects.filter(type=AssignmentTypes.SCHOOL, user=request.user).values_list('tid', flat=True)
        if mySchools.count() > 0:
            assignable['schools'] = School.objects.filter(id__in=mySchools).all()
        else:
            assignable['schools'] = None

    return render(request, 'attendance/assign.html', {
        'assignments': assignments,
        'targetuser': targetuser,
        'assignable': assignable,
        'is_facilitator': is_facilitator(targetuser),
        'is_mentor': is_mentor(targetuser)
    })