from django import forms

from mimesis.models import UserAlbum


class UserAlbumForm(forms.ModelForm):
    
    class Meta:
        model = UserAlbum
        exclude = ["user" ,"date_created"]
