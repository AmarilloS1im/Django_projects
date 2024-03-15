from django.shortcuts import render, HttpResponse, HttpResponseRedirect,redirect
from products.models import Product, Size, Basket, BasketQuerySet, FavoritesQuerySet, Favorites,ProductCategory
from products.forms import CheckboxForm
from products.context_processors import *










# Create your views here.
class IsChecked():
    def __init__(self,is_checked=True):
        self.is_checked = is_checked
def products(request, category_name=None):
    is_checked = IsChecked()


    baskets = Basket.objects.filter(user=request.user)
    favorites = Favorites.objects.filter(user=request.user).order_by('product')
    if category_name:
        category = ProductCategory.objects.get(name=category_name)
        products = Product.objects.filter(category=category).order_by('article')
    else:
        products = Product.objects.all().order_by('article')

    context = {
        'title': "Магазин",
        'footer_1': "127015, Москва, Бумажный пр-д., д. 14, стр. 2 ООО «НИКАМЕД».",
        'footer_2': "Копирование материалов запрещено.",
        'products': products,
        'sizes': Size.objects.all(),
        'baskets': baskets,
        'favorites': favorites,
        'categories':ProductCategory.objects.all()

    }

    context['is_checked'] = is_checked.is_checked


    return render(request, 'products/products.html', context)


def make_correct_url(http_refere):
    http_refere = http_refere.split('/')[3:]
    correct_url = ''
    for items in http_refere:
        if items != '':
            correct_url = correct_url + items + '/'
        else:
            pass
    print(correct_url)
    if correct_url == "products/":
        correct_url = "products/" + correct_url[:-1]+".html"
    else:
        correct_url = correct_url[:-1] + ".html"

    print(f"текущий адресс {correct_url}")

    return correct_url

def basket_add(request, product_id):

    http_referer = request.META['HTTP_REFERER']
    print(f"start add {http_referer}")
    make_correct_url(http_referer)

    baskets = Basket.objects.filter(user=request.user)
    favorites = Favorites.objects.filter(user=request.user).order_by('product')
    product = Product.objects.get(article=product_id)



    context = {
        'title': "Магазин",
        'footer_1': "127015, Москва, Бумажный пр-д., д. 14, стр. 2 ООО «НИКАМЕД».",
        'footer_2': "Копирование материалов запрещено.",
        'products': Product.objects.all().order_by('article'),
        'sizes': Size.objects.all(),
        # 'form': form,
        'baskets': baskets,
        'favorites': favorites,
        'categories': ProductCategory.objects.all()

    }
    #
    # if 'button_favorites' in request.POST:
    #     favorite = Favorites.objects.get(user=request.user, product=product_id)
    #     context['popup_product'] = favorite.product.article
    #     redirect_address = 'products/favorites.html'
    # else:
    #     redirect_address = "products/products.html"
    #     print(redirect_address)
    #     context['popup_product'] = product.article



    if request.method == 'POST':
        print('post')
        # if len(request.POST.getlist('checked_size_id')) < 1:
        #     is_checked = IsChecked(is_checked=False)
        #     context['is_checked'] = is_checked.is_checked
        #
        #     # return render(request, template_name=redirect_address, context= context)
        #     return HttpResponseRedirect(request.META['HTTP_REFERER'])

        # else:
        # is_checked = IsChecked(is_checked=True)
        # context['is_checked'] = is_checked.is_checked
        for article_size in request.POST.getlist('checked_size_id'):
            size = Size.objects.get(article_size=article_size)
            baskets = Basket.objects.filter(user=request.user, product=product, size=size)
            if not baskets.exists():
                Basket.objects.create(user=request.user, product=product, qty=1, size=size)
            else:
                basket = baskets.last()
                basket.qty += 1
                basket.save()
        # return render(request, template_name=redirect_address, context= context)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        # is_checked = IsChecked(is_checked=True)
        # context['is_checked'] = is_checked.is_checked
        print('not post')
        # return render(request, template_name=redirect_address, context= context)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])



def cart_add_plus_one(request, product_id, size_name):
    product = Product.objects.get(article=product_id)
    size = Size.objects.get(size_name=size_name, to_article=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product, size=size)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, qty=1, size=size)
    else:
        basket = baskets.last()
        basket.qty += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def cart_del_minus_one(request, basket_id):
    baskets = Basket.objects.filter(user=request.user, id=basket_id)
    basket = baskets.last()
    basket.qty -= 1
    basket.save()
    if basket.qty == 0:
        basket = Basket.objects.get(id=basket_id)
        basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def remove_all_user_baskets(request):
    all_user_baskets = Basket.objects.filter(user=request.user)
    all_user_baskets.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def item_info(request, product_id):
    product = Product.objects.get(article=product_id)
    context = {
        'title': "Магазин",
        'footer_1': "127015, Москва, Бумажный пр-д., д. 14, стр. 2 ООО «НИКАМЕД».",
        'footer_2': "Копирование материалов запрещено.",
        'product': product,
        'sizes': Size.objects.all(),
    }
    return render(request, 'products/item_info.html', context)


def cart(request):
    form = CheckboxForm()
    baskets = Basket.objects.filter(user=request.user)
    products = Product.objects.all()
    favorites  = Favorites.objects.filter(user=request.user).order_by('product')
    context = {
        'title': "Магазин",
        'footer_1': "127015, Москва, Бумажный пр-д., д. 14, стр. 2 ООО «НИКАМЕД».",
        'footer_2': "Копирование материалов запрещено.",
        'products':products,
        'sizes': Size.objects.all(),
        'form': form,
        'baskets': baskets,
        'favorites': favorites,
    }
    return render(request, 'products/cart.html', context)


def favorites(request):
    is_checked = IsChecked(is_checked=True)

    baskets = Basket.objects.filter(user=request.user)
    context = {
        'title': "Магазин",
        'footer_1': "127015, Москва, Бумажный пр-д., д. 14, стр. 2 ООО «НИКАМЕД».",
        'footer_2': "Копирование материалов запрещено.",
        'products': Product.objects.all(),
        'sizes': Size.objects.all(),
        'favorites': Favorites.objects.filter(user=request.user),
        'baskets': baskets,
        'current_page': 'favorites_page',
    }
    context['is_checked'] = is_checked.is_checked
    return render(request, 'products/favorites.html', context)


def favorites_add(request, product_id):

    product = Product.objects.get(article=product_id)


    favorites = Favorites.objects.filter(user=request.user, product=product)
    print(favorites)
    if not favorites.exists():
        favorite = Favorites.objects.create( user=request.user, product=product, qty=1, is_favorite=True)
        favorite.save()
        print(favorites)

    else:
        favorite = Favorites.objects.get(product=product_id,user=request.user)

        favorite.delete()
        print(favorites)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def favorites_remove(request, favorite_id):
    favorite = Favorites.objects.get(id=favorite_id,user=request.user)
    product = Product.objects.get(article=favorite.product.article)

    favorite.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def remove_all_user_favorites(request):
    all_user_favorites = Favorites.objects.filter(user=request.user)
    all_user_favorites.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def close_popup(request):
    is_checked = IsChecked()
    baskets = Basket.objects.filter(user=request.user)
    favorites = Favorites.objects.filter(user=request.user).order_by('product')


    context = {
        'title': "Магазин",
        'footer_1': "127015, Москва, Бумажный пр-д., д. 14, стр. 2 ООО «НИКАМЕД».",
        'footer_2': "Копирование материалов запрещено.",
        'products': Product.objects.all().order_by('article'),
        'sizes': Size.objects.all(),
        # 'form': form,
        'baskets': baskets,
        'favorites': favorites,

    }

    if 'button_favorites' in request.GET:

        redirect_address = 'products/favorites.html'
    else:
        redirect_address = 'products/products.html'

    return render(request, template_name=redirect_address, context=context)
    # return HttpResponseRedirect(request.META['HTTP_REFERER'])










