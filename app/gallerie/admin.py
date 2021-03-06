
from django.contrib import admin

from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.pages.admin import PageAdmin
from app.gallerie.models import Galleria, GalleriaImage


class GalleriaImageInline(TabularDynamicInlineAdmin):
    model = GalleriaImage
    readonly_fields = ('filename',)
    exclude = ('slug',)

class GalleriaAdmin(PageAdmin):

    class Media:
        css = {"all": ("css/admin/gallery.css",)}

    inlines = (GalleriaImageInline,)


admin.site.register(Galleria, GalleriaAdmin)
