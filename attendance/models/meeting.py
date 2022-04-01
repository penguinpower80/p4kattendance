from datetime import datetime

from django.core import serializers
from django.db import models

from attendance.models import AssignmentTypes
from attendance.models.notes import Notes
from django.contrib.auth.models import User

class Month(models.Model):
    number = models.IntegerField()

class Meeting(models.Model):
    date = models.DateField(default=datetime.now)
    type = models.TextField(max_length=1, choices=AssignmentTypes.choices, default='', blank=False, null=False)
    tid = models.CharField(max_length=50, blank=False, null=False)
    month = models.ForeignKey(Month, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
