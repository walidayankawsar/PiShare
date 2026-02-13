from django import forms
from .models import Session

class FileForm(forms.Form):
    class Meta:
        model = Session
        fields = ['file']