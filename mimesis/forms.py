from django import forms

from mimesis.models import Image, Audio


class ImageForm(forms.ModelForm):
    
    class Meta:
        model = Image
        exclude = ["user" ,"created"]


class AudioForm(forms.ModelForm):
    
    class Meta:
        model = Audio
        exclude = ["user", "date_created"]
