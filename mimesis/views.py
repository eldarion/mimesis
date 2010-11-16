from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from mimesis.forms import AlbumForm
from mimesis.models import Album, Photo


def index(request, template_name="mimesis/index.html", extra_context=None):
    
    if extra_context is None:
        extra_context = {}
    
    persona_photos, persona_albums = None, None
    
    if request.user.is_authenticated():
        persona = request.session.get("persona")
        if not persona:
            persona = request.user.get_profile()
        
        persona_photos = Photo.objects.with_owner(persona).order_by("-uploaded_on")
        
        ctype = ContentType.objects.get_for_model(persona)
        persona_albums = Album.objects.filter(
            owner_content_type__pk=ctype.id, 
            owner_id=persona.id
        ).order_by("-date_created")
    
    public_photos = Photo.objects.filter(
        private=False
    ).order_by("-uploaded_on")
    
    return render_to_response(template_name, dict({
        "persona_photos": persona_photos,
        "persona_albums": persona_albums,
        "public_photos": public_photos
    }, **extra_context), context_instance=RequestContext(request))


@login_required
def recent(request, template_name="mimesis/recent.html", extra_context=None):
    
    if extra_context is None:
        extra_context = {}
    
    PhotoFormSet = modelformset_factory(
        Photo,
        fields=["name", "description", "tags", "album", "private"],
        extra=0
    )
    
    if request.method == "POST":
        forms = PhotoFormSet(request.POST)
        if forms.is_valid():
            instances = forms.save(commit=False)
            for photo in instances:
                photo.new_upload = False
                photo.save()
    
    persona = request.session.get("persona")
    if not persona:
        persona = request.user.get_profile()
    
    ctype = ContentType.objects.get_for_model(persona)
    photos = Photo.objects.with_owner(persona).filter(
        new_upload=True
    ).order_by("-uploaded_on")
    
    if photos.count() == 0:
        return HttpResponseRedirect(reverse("mimesis_index"))
    
    formset = PhotoFormSet(queryset=photos)
    
    return render_to_response(template_name, dict({
        "photo_forms": formset,
    }, **extra_context), context_instance=RequestContext(request))


@login_required
def albums(request, form_class=AlbumForm, template_name="mimesis/albums.html", extra_context=None):
    
    if extra_context is None:
        extra_context = {}
    
    persona = request.session.get("persona")
    if not persona:
        persona = request.user.get_profile()
    
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.owner = persona
            album.save()
            return HttpResponseRedirect(reverse("mimesis_albums"))
    
    ctype = ContentType.objects.get_for_model(persona)
    albums = Album.objects.filter(
        owner_content_type__pk=ctype.id, 
        owner_id=persona.id
    ).order_by("-date_created")
    
    return render_to_response(template_name, dict({
        "albums": albums,
        "form": form_class()
    }, **extra_context), context_instance=RequestContext(request))


@login_required
def album(request, album_id, template_name="mimesis/album.html", extra_context=None):
    
    if extra_context is None:
        extra_context = {}
    
    persona = request.session.get("persona")
    if not persona:
        persona = request.user.get_profile()
    
    ctype = ContentType.objects.get_for_model(persona)
    album = Album.objects.get(
        id=album_id,
        owner_content_type__pk=ctype.id,
        owner_id=persona.id
    )
    photos = album.photo_set.all().order_by("-uploaded_on")
    
    return render_to_response(template_name, dict({
        "album": album,
        "photos": photos
    }, **extra_context), context_instance=RequestContext(request))


@login_required
def photo(request, photo_id, template_name="mimesis/photo.html", extra_context=None):
    
    if extra_context is None:
        extra_context = {}
    
    persona = request.session.get("persona")
    if not persona:
        persona = request.user.get_profile()
    
    ctype = ContentType.objects.get_for_model(persona)
    photo = Photo.objects.get(id=photo_id)
    if photo.private and photo.album.owner.user != persona.user:
        raise Http404
    
    return render_to_response(template_name, dict({
        "photo": photo,
    }, **extra_context), context_instance=RequestContext(request))


def upload_start(request, album_id=None):
    
    # @@@ Not sure this is the cleanest way to handle this however, template
    # @@@ authors should guard against showing an upload form to anonymous users
    if request.user.is_anonymous():
        return HttpResponseForbidden("You must be logged in to upload photos.")
    
    persona = request.session.get("persona")
    if not persona:
        persona = request.user.get_profile()
    
    if request.method == "POST" and request.FILES:
        a = None
        if album_id:
            try:
                ctype = ContentType.objects.get_for_model(persona)
                a = Album.objects.get(owner_id=persona.id, owner_content_type=ctype, id=album_id)
            except Album.DoesNotExist:
                pass
        
        for f in request.FILES.keys():
            p = Photo(
                photo=request.FILES[f],
                uploaded_by=request.user,
                album=a
            )
            p.save()
        
        if not getattr(settings, "MIMESIS_USE_FLASH_UPLOAD", False):
            return redirect(reverse("mimesis_recent"))
    
    return HttpResponse("OK")


def upload_complete(request):
    url = reverse("mimesis_recent")
    return HttpResponse("<a href=\"%s\">See Uploaded Photos</a>" % url)
