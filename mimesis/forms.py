from django import forms

from mimesis.models import Album


class AlbumForm(forms.ModelForm):
    
    class Meta:
        model = Album
        exclude = ["owner_id", "owner", "owner_content_type" ,"date_created"]
