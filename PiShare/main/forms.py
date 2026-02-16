from django import forms
from .models import Session

class FileForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['file']