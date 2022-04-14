from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def reports(request):
    context = {}
    return render(request, 'attendance/reports.html', context=context)

