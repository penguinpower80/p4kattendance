from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from attendance.models import Meeting
from attendance.utility import assignmentsFor, meetingsFor


@login_required
def home(request):
    user = request.user
    if not user.is_superuser:
        assignments = assignmentsFor(user, hierarchical=True)
        return render(request, 'attendance/home.html', {
            'assignments': assignments
        })
    else:
        return render(request, 'attendance/home.html')
