from copy import deepcopy
from django.contrib import admin
from mezzanine.galleries.admin import GalleryAdmin
from mezzanine.galleries.models import Gallery, GalleryImage


gallery_extra_fieldsets = ((None, {"fields": ("sold",)}),)
m_fieldsets = deepcopy(GalleryAdmin.fieldsets)
print(m_fieldsets[0][1]["fields"] )
#m_fieldsets[0][1]["fields"].insert(-1, "sold")

class MyGalleryAdmin(GalleryAdmin):
    fieldsets = m_fieldsets

admin.site.unregister(Gallery)
admin.site.register(Gallery, MyGalleryAdmin)
#
#from copy import deepcopy
#from django.contrib import admin
#from mezzanine.blog.admin import BlogPostAdmin
#from mezzanine.blog.models import BlogPost
#
#blog_fieldsets = deepcopy(BlogPostAdmin.fieldsets)
##print(blog_fieldsets )
#blog_fieldsets[0][1]["fields"].insert(-2, "image")
#
#class MyBlogPostAdmin(BlogPostAdmin):
#    fieldsets = blog_fieldsets
#
#admin.site.unregister(BlogPost)
#admin.site.register(BlogPost, MyBlogPostAdmin)
