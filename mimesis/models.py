from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from taggit.managers import TaggableManager


class Album(models.Model):
    
    owner_content_type = models.ForeignKey(ContentType)
    owner_id = models.PositiveIntegerField()
    owner = generic.GenericForeignKey("owner_content_type", "owner_id")
    
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    private = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return u"%s" % self.name
    
    @property
    def key_photo(self): # @@@ This should likely be set by the user
        photo = None
        for photo in self.photo_set.all().order_by("-uploaded_on"):
            break
        return photo


class PhotoManager(models.Manager):
    def with_owner(self, obj):
        ctype = ContentType.objects.get_for_model(obj)
        return super(PhotoManager, self).get_query_set().filter(
            album__owner_id=obj.id,
            album__owner_content_type__pk=ctype.id
        )


class Photo(models.Model):
    
    album = models.ForeignKey(Album)
    photo = models.ImageField(
        upload_to="mimesis/%Y/%m/%d",
        height_field="height",
        width_field="width"
    )
    width = models.IntegerField(blank=True)
    height = models.IntegerField(blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    private = models.BooleanField(default=False)
    new_upload = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(User)
    uploaded_on = models.DateTimeField(default=datetime.now)
    
    tags = TaggableManager()
    
    objects = PhotoManager()
    
    def next_or_prev(self, desc, **kwargs):
        order = "id"
        if desc:
            order = "-id"
        
        p = self.album.photo_set.filter(**kwargs).order_by(order)
        if p:
            return p[0]
        p = self.album.photo_set.all().order_by(order)
        if p:
            return p[0]
    
    def prev(self):
        return self.next_or_prev(desc=True, id__lt=self.id)
    
    def next(self):
        return self.next_or_prev(desc=False, id__gt=self.id)

