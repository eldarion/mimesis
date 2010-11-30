from django.contrib import admin

from mimesis.models import Image, ImageAssociation

admin.site.register(Image)
admin.site.register(ImageAssociation)