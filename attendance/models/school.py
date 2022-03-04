from django.db import models


class School(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=80)
    type = models.CharField(max_length=80, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
