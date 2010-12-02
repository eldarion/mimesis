from django import forms
from django.contrib.contenttypes.models import ContentType

from mimesis.models import Image, ImageAssociation
from mimesis.models import Audio, AudioAssociation


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        exclude = ("creator", "created",)
        
    def save(self, request, *args, **kwargs):
        self.instance.creator = request.user
        super(ImageForm, self).save(*args, **kwargs)


class ImageAssociationForm(forms.ModelForm):
    
    caption = forms.CharField()
    
    class Meta:
        model = ImageAssociation
        fields = ("caption",)
    
    def save(self, request, obj, image, *args, **kwargs):
        self.instance.content_type = ContentType.objects.get_for_model(obj)
        self.instance.object_pk = obj.pk
        self.image = image
        super(ImageAssociationForm, self).save(*args, **kwargs)


class AudioForm(forms.ModelForm):
    
    class Meta:
        model = Audio
        exclude = ("creator", "created",)
    
    def save(self, request, *args, **kwargs):
        self.instance.creator = request.user
        super(AudioForm, self).save(*args, **kwargs)


class AudioAssociationForm(forms.ModelForm):
    
    caption = forms.CharField()
    
    class Meta:
        model = AudioAssociation
        fields = ("caption",)
    
    def save(self, request, obj, audio, *args, **kwargs):
        self.instance.content_type = ContentType.objects.get_for_model(obj)
        self.instance.object_pk = obj.pk
        self.audio = audio
        super(AudioAssociationForm, self).save(*args, **kwargs)
