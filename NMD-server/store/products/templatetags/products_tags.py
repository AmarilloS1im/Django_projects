from django import template
from products.models import *
from products.views import *


register = template.Library()

@register.simple_tag()
def get_favorites(filter=None,filter_2=None):
    if not filter:

        return Favorites.objects.all()
    else:
        favorite = Favorites.objects.filter(user=filter,product=filter_2)
        if len(favorite) > 0:
            return favorite[0].is_favorite
        else:
            return False



# @register.inclusion_tag('products/size_form.html',takes_context=True)
# def form_data(context,filter=None,product_article=None):
#     if filter is True:
#         return {'form_data':True, 'product_article':product_article,'sizes':context['sizes']}
#     else:
#         return {'form_data':False,'product_article':"",'sizes':context['sizes']}



