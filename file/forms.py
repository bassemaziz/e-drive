from django import forms 
from .models import UserFile

class UploadFile(forms.ModelForm):

    class Meta:
        model = UserFile
        fields = ['file']

