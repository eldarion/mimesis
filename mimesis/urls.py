from django.conf.urls.defaults import patterns, url

from mimesis.views import index, album, upload_start


urlpatterns = patterns("mimesis.views",
    url(r'^$', view=index, name="mimesis_index"),
    url(r'^albums/$', view="albums", name="mimesis_albums"),
    url(r'^albums/(\d+)/$', view=album, name="mimesis_album"),
    url(r'^(\d+)/$', view="photo", name="mimesis_photo"),
    url(r'^recent/$', view="recent", name="mimesis_recent"),
    
    url(r"^uploads/upload/$", view=upload_start, name="mimesis_upload_start_url"),
    url(r"^uploads/upload/album/(\d+)/$", view=upload_start, name="mimesis_upload_start_album_url"),
    url(r"^uploads/complete/$", view="upload_complete", name="mimesis_upload_complete_url")
)
