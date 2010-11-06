from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from imagekit.models import ImageModel
from taggit.managers import TaggableManager

from mimesis.managers import ImageManager


class UserAlbum(models.Model):
    
    title = models.CharField(_("Album Title"), max_length=150)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User)
    date_created = models.DateTimeField(default=datetime.now)
    private = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u"%s" % self.title


class Image(ImageModel):
    
    title = models.CharField(max_length=150, null=True, blank=True)
    original_image = models.ImageField(upload_to="mimesis/%Y/%m/%d")
    num_views = models.PositiveIntegerField(editable=False, default=0)
    
    owner_content_type = models.ForeignKey(ContentType)
    owner_id = models.PositiveIntegerField()
    owner = generic.GenericForeignKey("owner_content_type", "owner_id")
    
    private = models.BooleanField(default=False)
    new_upload = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(User)
    uploaded_on = models.DateTimeField(default=datetime.now)
    
    tags = TaggableManager()
    objects = ImageManager()
    
    class IKOptions:
        image_field = "original_image"
        save_count_as = "num_views"
    
    def next_or_prev(self, desc, **kwargs):
        order = "id"
        if desc:
            order = "-id"
        
        p = self.owner.photo_set.filter(**kwargs).order_by(order)
        if p:
            return p[0]
        p = self.owner.photo_set.all().order_by(order)
        if p:
            return p[0]
    
    def prev(self):
        return self.next_or_prev(desc=True, id__lt=self.id)
    
    def next(self):
        return self.next_or_prev(desc=False, id__gt=self.id)
    


