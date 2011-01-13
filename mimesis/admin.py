from django.contrib import admin

from mimesis.models import FileUpload, FileAssociation

admin.site.register(FileUpload)
admin.site.register(FileAssociation)
