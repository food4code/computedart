from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader, Context
from mezzanine.conf import settings
from mezzanine.core.templatetags.mezzanine_tags import thumbnail
import glob
import codecs
import os
from django.core import management

def upload_list():
    file_dir = os.listdir(os.path.join(settings.MEDIA_ROOT ,'uploads'))

def slides_write(request, dir_name):

    size = (0, 600)

    cdir = os.path.dirname(os.path.abspath(__file__))
    file_dir = os.path.join(settings.MEDIA_ROOT ,'uploads', dir_name)
    template_file = os.path.join(cdir, 'static', dir_name + '.html')
    file_abs_list = sorted( glob.glob( os.path.join(file_dir , '*.jpg' )) )
    file_list = map(lambda f: '/'.join(f.split('/')[-3:]), file_abs_list)

    thumb_dir = os.path.join(file_dir, settings.THUMBNAILS_DIR_NAME)
    thumb_list = []

    for image_name in file_abs_list:
        thumb_image = os.path.join(thumb_dir, os.path.basename(image_name).replace(".", "-%sx%s." % size) )
        if not os.path.exists(thumb_image):
            print "Processing", thumb_image
            thumb_image = thumbnail(image_name, *size)
        #else:   print "skipping", thumb_image
        thumb_image = thumb_image.split('/static/')[1]
        thumb_list.append(thumb_image)

    print thumb_list

    t = loader.get_template('dtemplate.html')
    c = Context({
        'dir_name': dir_name,
        'file_list': thumb_list
    })
    template = t.render(c)
    #print template
    f = codecs.open(template_file, "w", "utf-8")
    f.write(template)
#    f.write()
    f.close()
    #management.call_command('collectstatic', interactive=False)

    return redirect("/static/" + dir_name + '.html')
    #return HttpResponse(template)

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