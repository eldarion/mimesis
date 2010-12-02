from django.contrib import admin

from mimesis.models import Image, ImageAssociation
from mimesis.models import Audio, AudioAssociation

admin.site.register(Image)
admin.site.register(ImageAssociation)

admin.site.register(Audio)
admin.site.register(AudioAssociation)