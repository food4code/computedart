
from mezzanine.pages.page_processors import processor_for
#from mezzanine.utils.views import paginate #we use our custom paginator to raise 404 for not existing pages
from .models import Galleria, GalleriaImage


from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import Http404

IMAGES_POST_PER_PAGE = 8 # TODO: Make it in default.py

def paginate(objects, page_num, per_page, max_paging_links):
    """
    Return a paginated page for the given objects, giving it a custom
    ``visible_page_range`` attribute calculated from ``max_paging_links``.
    """
    paginator = Paginator(objects, per_page)
    try:
        page_num = int(page_num)
    except ValueError:
        page_num = 1
    try:
        objects = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        raise Http404
    page_range = objects.paginator.page_range
    if len(page_range) > max_paging_links:
        start = min(objects.paginator.num_pages - max_paging_links,
            max(0, objects.number - (max_paging_links / 2) - 1))
        page_range = page_range[start:start + max_paging_links]
    objects.visible_page_range = page_range
    return objects

@processor_for(Galleria, exact_page=True)
def image_list(request, page):
    images = GalleriaImage.objects.all()
    MAX_PAGING_LINKS = int(len(images)/IMAGES_POST_PER_PAGE)
    print()
    images = paginate(images, request.GET.get("page", 1),
                        IMAGES_POST_PER_PAGE,
                        MAX_PAGING_LINKS)
    return { "images": images }
