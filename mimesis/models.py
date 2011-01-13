import datetime
import mimetypes

from django.db import models

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from mimesis.managers import MediaAssociationManager
from taggit.managers import TaggableManager


class FileUpload(models.Model):
    
    title = models.CharField(max_length=150)
    description = models.TextField()
    file = models.FileField(upload_to="mimesis")
    creator = models.ForeignKey(User)
    created = models.DateTimeField(default=datetime.datetime.now)
    type = models.CharField(editable=False, max_length=100)
    subtype = models.CharField(editable=False, max_length=100)
    
    tags = TaggableManager()
    
    def __unicode__(self):
        return self.title
    
    @property
    def mime_type(self):
        return "%s/%s" % (self.type, self.subtype)
    
    def save(self, *args, **kwargs):
        (mime_type, encoding) = mimetypes.guess_type(self.upload.path)
        try:
            mime = mime_type.split("/")
            self.type = mime[0]
            self.subtype = mime[1]
        except:
            # Mime type unknown, use text/plain
            self.type = "text"
            self.sub_type = "plain"
        super(UploadedFile, self).save()


class FileAssociation(models.Model):
    """
    A generic association of a FileUpload object and any other Django model.
    """
    
    content_type = models.ForeignKey(ContentType)
    object_pk = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey("content_type", "object_pk")
    description = models.TextField()
    
    objects = FileAssociationManager()
