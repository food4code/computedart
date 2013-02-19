import shutil
from PIL import Image
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader, Context
from mezzanine.conf import settings
from mezzanine.core.templatetags.mezzanine_tags import thumbnail
import glob
import codecs
import os
import zipfile
from app.gallerie.models import Galleria, GalleriaImage
from mezzanine.core.fields import FileField
from django.core.files.base import ContentFile
from django.core.files import File

def upload_list():
    image_dir = os.listdir(os.path.join(settings.MEDIA_ROOT ,'uploads'))



def make_thumb(image_abs_list, image_dir):
    MAXWIDTH = 980
    MAXHEIGHT = 600
    DELTA = 50
    thumb_dir = os.path.join(image_dir, settings.THUMBNAILS_DIR_NAME)
    thumb_list = []

    for image_name in image_abs_list:
        image_base = os.path.basename(image_name)

        img = Image.open(image_name)
        w, h = img.size
        if w == h or abs(w - h) < DELTA:
            size = (MAXHEIGHT, MAXHEIGHT)
        elif w > h: #landscape image
            if w / float(h) > 1.5:
                size = (MAXWIDTH, 0)
            else:
                size = (0, MAXHEIGHT)
        else:
            size = (0, MAXHEIGHT)
        image_base = os.path.splitext(image_base)
        thumb_image = os.path.join(thumb_dir, image_base[0]+ "-%sx%s" % size+ image_base[1])
        if not os.path.exists(thumb_image):
            print "Processing", thumb_image
            thumb_image = thumbnail(image_name, *size)
        #else:   print "skipping", thumb_image
        thumb_list.append(os.path.basename(thumb_image))

        ### Move original file
        orig_dir = os.path.join(image_dir, 'orig')
        if not os.path.exists(orig_dir):
            os.makedirs(orig_dir)
        shutil.move(image_name, orig_dir)

    return thumb_list

def slides_write(request, dir_name):

    cdir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(settings.MEDIA_ROOT ,'uploads', dir_name)
    template_file = os.path.join(cdir, 'static', dir_name + '.html')
    image_abs_list = sorted( glob.glob( os.path.join(image_dir , '*.jpg' )) )
    thumb_dir = os.path.join(image_dir, settings.THUMBNAILS_DIR_NAME)

    gal = Galleria.objects.filter(title=dir_name)
    image_list = []
    if not gal:
        image_list = make_thumb(image_abs_list, image_dir)
        zip_name = os.path.join(settings.MEDIA_ROOT, dir_name+'.zip')
        zip = zipfile.ZipFile(zip_name, 'w')
        for im in glob.glob( os.path.join(thumb_dir , '*.jpg' )):
            zip.write(im, os.path.basename(im))
        zip.close()
        gal = Galleria.objects.create(title=dir_name, zip_import=zip_name)
        gal.save()

    else:
        print "*****************************"
        ### TODO: check for new files
        gal = Galleria.objects.get(title=dir_name)

        for gi in gal.images.all():
            image_list.append(gi.file.filename)

    image_list = map(lambda img: os.path.join(image_dir.split('/static/')[1], img), image_list )

    print image_list

    t = loader.get_template('dtemplate.html')
    c = Context({
        'dir_name': dir_name,
        'file_list': image_list
    })
    template = t.render(c)
    f = codecs.open(template_file, "w", "utf-8")
    f.write(template)
    f.close()

    return redirect("/static/" + dir_name + '.html')

def slides_send(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename="template.html"'

    file_list = (
    )

    t = loader.get_template('dtemplate.html')
    c = Context({
        'data': file_list
    })
    response.write(t.render(c))
    return response