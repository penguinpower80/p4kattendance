from django.contrib.auth.models import User
from django.db import models

class AssignmentTypes(models.TextChoices):
    MENTOR = 'M', 'Mentor'
    SCHOOL = 'S', 'School'
    CLASSROOM = 'C', 'Classroom'
    STUDENT = 'P', 'Student'

class Assignments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tid = models.CharField(max_length=50, blank=False, null=False)
    type = models.TextField(max_length=1, choices=AssignmentTypes.choices, default='', blank=False, null=False)
    def __str__(self):
        return f'{self.user.username} - {self.get_type_display()} #{self.tid}'

    class Meta:
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'