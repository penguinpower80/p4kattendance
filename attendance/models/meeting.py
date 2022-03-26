from django.db import models

from attendance.models.notes import Notes
from django.contrib.auth.models import User

class Month(models.Model):
    number = models.IntegerField()

class Meeting(models.Model):
    meeting_id = models.CharField(max_length=15, primary_key=True)
    date = models.DateField()
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.ForeignKey(Notes, on_delete=models.CASCADE, related_name="meeting_notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)