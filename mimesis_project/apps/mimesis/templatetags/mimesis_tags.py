from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_unicode

from mimesis.models import ImageAssociation, AudioAssociation, VideoAssociation

register = template.Library()


class BaseMediaNode(template.Node):
    """
    Base helper class (abstract) for handling the get_media_for template tags.
    """

    @classmethod
    def handle_token(cls, parser, token, model):
        """Class method to parse get_media_list and return a Node."""
        
        tokens = token.contents.split()
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])

        # {% get_whatever for obj as varname %}
        if len(tokens) == 5:
            if tokens[3] != 'as':
                raise template.TemplateSyntaxError("Third argument in %r must be 'as'" % tokens[0])
            return cls(
                object_expr = parser.compile_filter(tokens[2]),
                as_varname = tokens[4],
                model = model,
            )

        # {% get_whatever for app.model pk as varname %}
        elif len(tokens) == 6:
            if tokens[4] != 'as':
                raise template.TemplateSyntaxError("Fourth argument in %r must be 'as'" % tokens[0])
            return cls(
                ctype = BaseMediaNode.lookup_content_type(tokens[2], tokens[0]),
                object_pk_expr = parser.compile_filter(tokens[3]),
                as_varname = tokens[5],
                model = model,
            )

        else:
            raise template.TemplateSyntaxError("%r tag requires 4 or 5 arguments" % tokens[0])

    @staticmethod
    def lookup_content_type(token, tagname):
        try:
            app, model = token.split('.')
            return ContentType.objects.get(app_label=app, model=model)
        except ValueError:
            raise template.TemplateSyntaxError("Third argument in %r must be in the format 'app.model'" % tagname)
        except ContentType.DoesNotExist:
            raise template.TemplateSyntaxError("%r tag has non-existant content-type: '%s.%s'" % (tagname, app, model))

    def __init__(self, ctype=None, object_pk_expr=None, object_expr=None, as_varname=None, model=None):
        if ctype is None and object_expr is None:
            raise template.TemplateSyntaxError("Media nodes must be given either a literal object or a ctype and object pk.")
        self.media_model = model
        self.as_varname = as_varname
        self.ctype = ctype
        self.object_pk_expr = object_pk_expr
        self.object_expr = object_expr

    def render(self, context):
        qs = self.get_query_set(context)
        context[self.as_varname] = self.get_context_value_from_queryset(context, qs)
        return ""

    def get_query_set(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        if not object_pk:
            return self.media_model.objects.none()

        qs = self.media_model.objects.filter(
            content_type = ctype,
            object_pk    = smart_unicode(object_pk),
        )

        return qs

    def get_target_ctype_pk(self, context):
        if self.object_expr:
            try:
                obj = self.object_expr.resolve(context)
            except template.VariableDoesNotExist:
                return None, None
            return ContentType.objects.get_for_model(obj), obj.pk
        else:
            return self.ctype, self.object_pk_expr.resolve(context, ignore_failures=True)

    def get_context_value_from_queryset(self, context, qs):
        """Subclasses should override this."""
        raise NotImplementedError


class MediaListNode(BaseMediaNode):
    """Insert a list of media into the context."""
    def get_context_value_from_queryset(self, context, qs):
        return list(qs)


@register.tag
def get_images_for(parser, token):
    return MediaListNode.handle_token(parser, token, ImageAssociation)


@register.tag
def get_audio_for(parser, token):
    return MediaListNode.handle_token(parser, token, AudioAssociation)


@register.tag
def get_videos_for(parser, token):
    return MediaListNode.handle_token(parser, token, VideoAssociation)
