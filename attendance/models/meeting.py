from datetime import datetime
from django.db import models
from attendance.models import AssignmentTypes
from django.contrib.auth.models import User

class Meeting(models.Model):
    date = models.DateField(default=datetime.now)
    type = models.TextField(max_length=1, choices=AssignmentTypes.choices, default='', blank=False, null=False)
    tid = models.CharField(max_length=50, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
