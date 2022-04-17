import logging

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from attendance.forms import ProfileForm
from attendance.utility import getRedirectWithParam, is_mentor


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    mentors = User.objects.filter(groups__name='Mentors')
    facilitators = User.objects.filter(groups__name='Facilitators')
    msg = request.GET.get('msg', None)
    return render(request, 'attendance/users.html', {
        'mentors': mentors,
        'facilitators': facilitators,
        'message': msg,
    })

def adduser(request, type='mentor'):
    if type != 'mentor' and type != 'facilitator':
        return HttpResponse(status=401)
    form = ProfileForm(request.POST or None, initial={'usertype': type, 'user_id':'NEW'})

    if request.method == "POST":
        if form.is_valid():
            user = User.objects.create_user(
                request.POST.get('username'),
                request.POST.get('email'),
                request.POST.get('newpassword')
            )
            user.first_name= request.POST.get('first')
            user.last_name=request.POST.get('last')
            user.is_active = request.POST.get('useractive') == '1'
            user.save()
            if request.POST.get('usertype') == 'mentor':
                group = Group.objects.get(name='Mentors')
            else:
                group = Group.objects.get(name='Facilitators')
            group.user_set.add(user)
            return getRedirectWithParam('User added.', 'attendance:users')
        else:
            return render(request, 'attendance/adduser.html', {'form': form, 'type': type})

    return render(request, 'attendance/adduser.html', { 'form': form, 'type': type } )

def edituser(request, id):
    user = get_object_or_404(User, pk=id)

    if is_mentor(user):
        type='mentor'
    else:
        type='facilitator'

    form = ProfileForm(request.POST or None, initial={
        'username': user.username,
        'usertype': type,
        'first': user.first_name,
        'last': user.last_name,
        'email': user.email,
        'useractive': '1' if user.is_active else '0',
        'user_id': user.id
    })

    if request.method == "POST":
        if form.is_valid():
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.first_name= request.POST.get('first')
            user.last_name=request.POST.get('last')
            user.is_active = request.POST.get('useractive') == '1'
            user.set_password(request.POST.get('newpassword'))
            user.save()
            user.groups.clear()
            if request.POST.get('usertype') == 'mentor':
                group = Group.objects.get(name='Mentors')
            else:
                group = Group.objects.get(name='Facilitators')
            group.user_set.add(user)

            return getRedirectWithParam('User updated.', 'attendance:users')
        else:
            return render(request, 'attendance/edituser.html', {'form': form, 'type': type, 'id': id})

    return render(request, 'attendance/edituser.html', { 'form': form, 'id':id } )




def deleteuser(request, id):
    user = get_object_or_404(User, pk=id)
    user.delete()
    return getRedirectWithParam('User deleted.', 'attendance:users')