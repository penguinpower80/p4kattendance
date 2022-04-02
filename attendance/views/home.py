from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from attendance.forms import NotesForm
from attendance.utility import assignmentsFor


@login_required
def home(request):
    user = request.user
    msg = request.GET.get('msg', None)
    if not user.is_superuser:
        notesform = NotesForm()
        assignments = assignmentsFor(user, hierarchical=True)
        return render(request, 'attendance/home.html', {
            'assignments': assignments,
            'message': msg,
            'notesform': notesform
        })
    else:
        return render(request, 'attendance/home.html')
