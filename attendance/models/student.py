from django.db import models

from attendance.models import Classroom


class Gender(models.TextChoices):
    FEMALE = 'F', 'Female'
    MALE = 'M', 'Male'


class Student(models.Model):
    nde_id = models.CharField(max_length=10, null=False, blank=False, primary_key=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='classroom')
    dob = models.DateField(null=True, blank=True)
    gender = models.TextField(max_length=1, choices=Gender.choices, default='', blank=True, null=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zip = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
