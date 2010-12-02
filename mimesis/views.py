from django.db.models import get_model
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required

from mimesis.forms import ImageForm, ImageAssociationForm
from mimesis.forms import AudioForm, AudioAssociationForm
from mimesis.models import Image, Audio, Video


@login_required
@require_POST
def add_image(request, template_name="mimesis/image_add.html", 
              app_label=None, model_name=None, obj_pk=None):
    
    if obj_pk:
        model = get_model(app_label, model_name)
        obj = get_object_or_404(model, pk=obj_pk)
    
    next = request.POST.get("next", "/")
    
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        image = form.save(request)
        return HttpResponseRedirect(next)
    else:
        return render_to_response(template_name, {
            "form": form,
        }, RequestContext(request))


@login_required
@require_POST
def associate_image(request, pk, app_label, model_name, obj_pk):
    
    next = request.POST.get("next", "/")
        
    model = get_model(app_label)
    obj = get_object_or_404(model, pk=obj_pk)
    image = get_object_or_404(Image, pk=pk)
    
    form = ImageAssociationForm(request.POST)
    if form.is_valid():
        form.save(request, obj, image)
        return HttpResponseRedirect(next)
    else:
        return render_to_response("/", {
            "form": form,
        }, RequestContext(request))

