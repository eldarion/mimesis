import datetime

from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from mimesis.managers import MediaAssociationManager
from taggit.managers import TaggableManager


class MediaBase(models.Model):
    
    title = models.CharField(max_length=150)
    created = models.DateTimeField(default=datetime.datetime.now)
    
    tags = TaggableManager()
    
    class Meta:
        abstract = True


class MediaAssociationBase(models.Model):
    
    owner_content_type = models.ForeignKey(ContentType)
    owner_object_id = models.PositiveIntegerField()
    owner = generic.GenericForeignKey("owner_content_type", "owner_object_id")
    
    caption = models.TextField(blank=True)
    
    objects = MediaAssociationManager()
    
    class Meta:
        abstract = True


class Image(MediaBase):
    
    image = models.ImageField(upload_to="mimesis/image/")


class ImageAssociation(MediaAssociationBase):
    
    image = models.ForeignKey(Image)


class Audio(MediaBase):
    
    audio = models.FileField(upload_to="mimesis/audio/")


class AudioAssociation(MediaAssociationBase):
    
    audio = models.ForeignKey(Audio)


class Video(MediaBase):
    
    video = models.URLField(blank=True)


class VideoAssociation(MediaAssociationBase):
    
    video = models.ForeignKey(Video)
