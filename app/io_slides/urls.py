from django.conf.urls.defaults import patterns, url
#from django.conf import settings
from mezzanine.conf import settings
urlpatterns = patterns("",
    url(r'^view/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.STATIC_ROOT,
        }),
    url(r'^(?P<dir_name>\w+)$',
        "io_slides.views.slides_write", name="slides"),

    )