from django.contrib import admin

from mimesis.models import MediaUpload, MediaAssociation

admin.site.register(MediaUpload)
admin.site.register(MediaAssociation)
