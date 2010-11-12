from django import forms

from mimesis.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ["user" ,"date_created"]


# class AudioForm(forms.ModelForm):
#     
#     class Meta:
#         model = Audio
#         exclude = ["user", "date_created"]
# 
# class VideoForm(forms.ModelForm):
#     
#     class Meta:
#         model = Video
#         exclude = ["user", "date_created"]
