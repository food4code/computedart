
from cStringIO import StringIO
import os
from string import punctuation
from urllib import unquote
from zipfile import ZipFile

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse, resolve

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings
from mezzanine.core.fields import FileField
from mezzanine.core.models import Orderable, RichText, Slugged
from mezzanine.pages.models import Page
from mezzanine.utils.importing import import_dotted_path
from mezzanine.utils.models import upload_to
from mezzanine.utils.urls import slugify
from mezzanine.core.managers import SearchableManager


# Set the directory where gallery images are uploaded to,
# either MEDIA_ROOT + 'galleries', or filebrowser's upload
# directory if being used.
GALLERIES_UPLOAD_DIR = "galleries"
if settings.PACKAGE_NAME_FILEBROWSER in settings.INSTALLED_APPS:
    fb_settings = "%s.settings" % settings.PACKAGE_NAME_FILEBROWSER
    try:
        GALLERIES_UPLOAD_DIR = import_dotted_path(fb_settings).DIRECTORY
    except ImportError:
        pass


class Galleria(Page, RichText):
    """
    Page bucket for gallery photos.
    """

    zip_import = models.FileField(verbose_name=_("Zip import"), blank=True,
        upload_to=upload_to("galleries.Galleria.zip_import", "galleries"),
        help_text=_("Upload a zip file containing images, and "
                    "they'll be imported into this gallery."))
    class Meta:
        verbose_name = _("Galleria")
        verbose_name_plural = _("Gallerie")

    def save(self, delete_zip_import=True, *args, **kwargs):
        """
        If a zip file is uploaded, extract any images from it and add
        them to the gallery, before removing the zip file.
        """
        super(Galleria, self).save(*args, **kwargs)
        if self.zip_import:
            zip_file = ZipFile(self.zip_import)
            # import PIL in either of the two ways it can end up installed.
            try:
                from PIL import Image
            except ImportError:
                import Image
            for name in zip_file.namelist():
                data = zip_file.read(name)
                try:
                    image = Image.open(StringIO(data))
                    image.load()
                    image = Image.open(StringIO(data))
                    image.verify()
                except:
                    continue
                path = os.path.join(GALLERIES_UPLOAD_DIR, self.slug,
                                    name.decode("utf-8"))
                try:
                    saved_path = default_storage.save(path, ContentFile(data))
                except UnicodeEncodeError:
                    from warnings import warn
                    warn("A file was saved that contains unicode "
                         "characters in its path, but somehow the current "
                         "locale does not support utf-8. You may need to set "
                         "'LC_ALL' to a correct value, eg: 'en_US.UTF-8'.")
                    path = os.path.join(GALLERIES_UPLOAD_DIR, self.slug,
                                        unicode(name, errors="ignore"))
                    saved_path = default_storage.save(path, ContentFile(data))
                self.images.add(GalleriaImage(file=saved_path))
            if delete_zip_import:
                zip_file.close()
                self.zip_import.delete(save=True)


class GalleriaImage(Orderable, Slugged):

    gallery = models.ForeignKey("Galleria", related_name="images")
    file = FileField(_("File"), max_length=200, format="Image",
        upload_to=upload_to("classic.GalleriaImage.file", "galleries"))
#    title = models.CharField("Title", max_length=40, blank=True)
    description = models.CharField(_("Description"), max_length=500, blank=True)
    sold = models.IntegerField(_("items sold"), max_length=3, null=True, blank=True )
    notes = models.TextField(_("Notes"), blank=True)
    filename = models.CharField("filename", max_length=30, blank=True) #editable=False,


    objects = SearchableManager()
    search_fields = ("title", "description")
#    search_fields = {"title":5, "description":3, "filename":2, "notes":2}

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        If no description is given when created, create one from the
        file name.
        """
        if not self.id:

            name = unquote(self.file.url).split("/")[-1]
            self.filename = name
            name = name.rsplit(".", 1)[0].replace("'", "")
            name = "".join([c if c not in punctuation else " " for c in name])
            # str.title() doesn't deal with unicode very well.
            # http://bugs.python.org/issue6412
            name = "".join([s.upper() if i == 0 or name[i - 1] == " " else s
                            for i, s in enumerate(name)])
            if not self.title:
                self.title = name
            if not self.sold:
                self.sold = 0

        super(GalleriaImage, self).save(*args, **kwargs)

    #@models.permalink
    def get_absolute_url(self):
        url =  self.file.url
        return url
#        return reverse("image_detail", kwargs={"slug": self.slug})
