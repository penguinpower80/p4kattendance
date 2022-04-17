from ckeditor.widgets import CKEditorWidget
from django import forms


class NotesForm(forms.Form):
    Note = forms.CharField(widget=CKEditorWidget(), label=False)

