from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager

from mimesis.managers import MediaManager


class MediaBase(models.Model):
    """
    An abstract base class for attachable media.
    """
    
    title = models.CharField(max_length=150, null=True, blank=True)
    user = models.ForeignKey(User)
    date_created = models.DateTimeField(default=datetime.now)
    private = models.BooleanField(default=False)
    
    owner_content_type = models.ForeignKey(ContentType)
    owner_id = models.PositiveIntegerField()
    owner = generic.GenericForeignKey("owner_content_type", "owner_id")
    
    tags = TaggableManager()
    objects = MediaManager()
    
    class Meta:
        abstract = True


class Image(MediaBase):
    image = models.ImageField(upload_to="mimesis/%Y/%m/%d")
    
    def __unicode__(self):
        return u"Image for %s" % self.owner
    
    def next_or_prev(self, desc, **kwargs):
        order = "id"
        if desc:
            order = "-id"
        
        p = self.owner.image_set.filter(**kwargs).order_by(order)
        if p:
            return p[0]
        p = self.owner.image_set.all().order_by(order)
        if p:
            return p[0]
    
    def prev(self):
        return self.next_or_prev(desc=True, id__lt=self.id)
    
    def next(self):
        return self.next_or_prev(desc=False, id__gt=self.id)


# class Audio(MediaBase):
#     
#     def __unicode__(self):
#         return u"Audio"
# 
# 
# class Video(models.Model):
#     
#     def __unicode__(self):
#         return u"Video"
