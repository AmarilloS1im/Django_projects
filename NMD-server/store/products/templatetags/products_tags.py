from django import template
from products.views import Favorites


register = template.Library()


@register.simple_tag()
def get_favorites(filter=None, filter_2=None):
    if not filter:
        return Favorites.objects.all()
    else:
        favorite = Favorites.objects.filter(user=filter, product=filter_2)
        if len(favorite) > 0:
            return favorite[0].is_favorite
        else:
            return False
