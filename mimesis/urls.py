from django.conf.urls.defaults import patterns, url


urlpatterns = patterns("upload.views",
    
    # Images
    url(r"^/image/add/", "add_image", name="add_image"),
    url(r"^/image/add-for/(?P<app_label>[\w\-]+)/(?P<module_name>[\w\-]+)/(?P<obj_pk>\d+)/$",
        "add_image", name="add_image_for"),
    url(r"^/image/(?P<pk>\d+)/associate/(?P<app_label>[\w\-]+)/(?P<module_name>[\w\-]+)/(?P<obj_pk>\d+)/$",
        "associate_image", name="associate_image"),
    
    # Audio
    # url(r"^/audio/add/", "add_audio", name="add_audio"),
    # url(r"^/audio/add-for/(?P<app_label>[\w\-]+)/(?P<module_name>[\w\-]+)/(?P<obj_pk>\d+)/$",
    #     "add_audio", name="add_audio_for"),
    # url(r"^/audio/(?P<pk>\d+)/associate/(?P<app_label>[\w\-]+)/(?P<module_name>[\w\-]+)/(?P<obj_pk>\d+)/$",
    #     "associate_audio", name="associate_audio"),
)