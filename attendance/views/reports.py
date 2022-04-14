from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def report(request):
    context = {}
    return render(request, 'attendance/reports.html', context=context)

