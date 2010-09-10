from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from taggit.managers import TaggableManager


class Album(models.Model):
    
    owner = models.ForeignKey(User)
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


class Photo(models.Model):
    
    album = models.ForeignKey(Album, null=True, blank=True)
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
    
    def next_or_prev(self, desc, **kwargs):
        order = "id"
        if desc:
            order = "-id"
        
        if self.album:
            p = self.album.photo_set.filter(**kwargs).order_by(order)
            if p:
                return p[0]
            p = self.album.photo_set.all().order_by(order)
            if p:
                return p[0]
        else:
            p = self.uploaded_by.photo_set.filter(**kwargs).order_by(order)
            if p:
                return p[0]
            p = self.uploaded_by.photo_set.all().order_by(order)
            if p:
                return p[0]
    
    def prev(self):
        return self.next_or_prev(desc=True, id__lt=self.id)
    
    def next(self):
        return self.next_or_prev(desc=False, id__gt=self.id)

