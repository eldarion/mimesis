from django import forms

from mimesis.models import Album


class AlbumForm(forms.ModelForm):
    
    class Meta:
        model = Album
        exclude = ["owner", "date_created"]
