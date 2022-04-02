from django.db import models

from django.contrib.auth.models import User

from attendance.models import AssignmentTypes


class Notes(models.Model):
    type = models.TextField(max_length=1, choices=AssignmentTypes.choices, default='', blank=False, null=False)
    tid = models.CharField(max_length=50, blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, null=True, blank=True)
    visible = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} - {self.created_at}'

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'