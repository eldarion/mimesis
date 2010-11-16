from django.db import models

from django.contrib.contenttypes.models import ContentType


class MediaManager(models.Manager):
    
    def for_model(self, model, content_type=None):
        content_type = content_type or ContentType.objects.get_for_model(model)
        kwargs = {
            self.owner_content_type: content_type,
            self.owner_id: model.pk
        }
        objects = self.get_query_set().filter(**kwargs)
        return objects
