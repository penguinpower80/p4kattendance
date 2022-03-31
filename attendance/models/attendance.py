from django.contrib.auth.models import User
from django.db import models

from attendance.models import Student, Meeting

class AttendanceStatus(models.TextChoices):
    PRESENT = 'p', 'Present'
    ABSENT = 'a', 'Absent'
    TARDY = 't', 'Tardy'

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    status = models.TextField(max_length=1, choices=AttendanceStatus.choices, default='p')

    def __str__(self):
        return f'{self.meeting.date} - {self.student.nde_id} - {self.get_status_display()}'
