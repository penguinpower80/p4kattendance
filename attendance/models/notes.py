from django.db import models

from django.contrib.auth.models import User


class Notes(models.Model):
    note_id = models.CharField(max_length=15, primary_key=True)
    note_type = models.CharField(max_length=20, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    note_text = models.TextField(max_length=500, null=True, blank=True)
    note_visible = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}'