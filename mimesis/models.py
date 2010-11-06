from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from imagekit.models import ImageModel

from taggit.managers import TaggableManager


class Album(models.Model):
    
    title = models.CharField(_("Album Title"), max_length=150)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(default=datetime.now)
    private = models.BooleanField(default=False)
    
    owner_user = models.ForeignKey(User, null=True, related_name="photo_albums")
    
    owner_content_type = models.ForeignKey(ContentType)
    owner_id = models.PositiveIntegerField()
    owner_object = generic.GenericForeignKey("owner_content_type", "owner_id")
    
    @property
    def key_photo(self): # @@@ This should likely be set by the user
        photo = None
        for photo in self.photos.all().order_by("-uploaded_on"):
            break
        return photo
    
    @property
    def owner(self):
        return self.owner_user or self.owner
    
    def __unicode__(self):
        return u"%s" % self.name


class PhotoManager(models.Manager):
    def with_owner(self, obj):        
        ctype = ContentType.objects.get_for_model(obj)
        return super(PhotoManager, self).get_query_set().filter(
            album__owner_id=obj.id,
            album__owner_content_type__pk=ctype.id
        )


class Photo(ImageModel):
    title = models.CharField(max_length=150, null=True, blank=True)
    original_image = models.ImageField(upload_to="mimesis/%Y/%m/%d")
    num_views = models.PositiveIntegerField(editable=False, default=0)
    
    album = models.ForeignKey(Album, related_name="album")
    private = models.BooleanField(default=False)
    new_upload = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(User)
    uploaded_on = models.DateTimeField(default=datetime.now)
    
    tags = TaggableManager()
    objects = PhotoManager()
    
    class IKOptions:
        image_field = "original_image"
        save_count_as = "num_views"
    
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
    


