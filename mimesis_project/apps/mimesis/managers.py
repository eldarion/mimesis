from django.db import models

from django.contrib.contenttypes.models import ContentType


class MediaAssociationManager(models.Manager):
    
    def for_model(self, model, content_type=None):
        content_type = content_type or ContentType.objects.get_for_model(model)
        objects = self.get_query_set().filter(
            owner_content_type=content_type, 
            owner_object_id=model.pk,
        )
        return objects
