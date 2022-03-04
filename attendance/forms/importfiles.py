from django import forms
#from django.forms import models
from django.core.exceptions import ValidationError
from django.db import models

def validate_file_extension(value):
    if not value.name.endswith('.csv'):
        raise ValidationError(u'Invalid File Extension')

class FileType(models.TextChoices):
    STUDENT = 'student', 'Student File'
    SCHOOL = 'school', 'School File'

class ImportFileForm(forms.Form):
    filetype = forms.ChoiceField(label='File Type', choices=FileType.choices)
    file = forms.FileField(label='Select File', validators=[validate_file_extension])


