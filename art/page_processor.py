
from mezzanine.pages.page_processors import processor_for
from mezzanine.utils.views import render, paginate
from mezzanine.galleries.models import Gallery
from django.http import HttpResponseRedirect
#@processor_for(Gallery)
@processor_for(Gallery)
def exibitions(request, page):
    print('****************         ***************************************')
    raise Exception('spam', 'eggs')
    i = request.GET.get("i", 1)
    i = int(i)+1
    return {"i":i}
