from django.db import models

from attendance.models.school import School


class Classroom(models.Model):
    name = models.CharField(max_length=80)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} at {self.school.name}'
