from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from products.context_processors import Basket, Favorites, Product, Size
from store.utils import DataMixin

# Create your views here.


def products(request, page=1):
    filter_dict = {'category__in': ['Shoe', 'Clothes'],
                   'product_type__in': ['Boots', 'Longboots', 'Short_boots', 'Pullover', 'Sneakers'],
                   'gender__in': ['Male', 'Female'], 'season__in': ['Winter', 'Summer'],
                   'age__in': ['Adult', 'Child'], }

    if request.method == 'POST':
        filters = request.POST.getlist('filter_id')
        if len(filters) > 0:
            filter_param_list = []
            for items in filters:
                for k, v in filter_dict.items():
                    if items in filter_dict[k]:
                        filter_param_list.append(k)
                        break
            request.session['filters'] = filters
            current_filters = request.session['filters']
            param_dict = {}
            for param_name in filter_param_list:
                param_dict[param_name] = current_filters
            products = Product.objects.filter(**param_dict).order_by('article')
        else:
            if 'filters' in request.session:
                if request.session['filters']:
                    filter_param_list = []
                    for items in request.session['filters']:
                        for k, v in filter_dict.items():
                            if items in filter_dict[k]:
                                filter_param_list.append(k)
                                break
                    current_filters = request.session['filters']
                    param_dict = {}
                    for param_name in filter_param_list:
                        param_dict[param_name] = current_filters
                    products = Product.objects.filter(**param_dict).order_by('article')
                else:
                    products = Product.objects.all().order_by('article')
            else:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])

        paginator = Paginator(products, per_page=3)
        products_paginator = paginator.page(page)
        context = {
            'title': "Магазин",
            'products': products_paginator,
        }

        return render(request, 'products/products.html', context)
    else:
        products = Product.objects.all().order_by('article')
        paginator = Paginator(products, per_page=3)
        products_paginator = paginator.page(page)
        context = {
            'title': "Магазин",
            'products': products_paginator,
        }
        return render(request, 'products/products.html', context)


def reset_filters(request):
    request.session['filters'] = []
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_add(request, product_id):
    product = Product.objects.get(article=product_id)
    if request.method == 'POST':
        for article_size in request.POST.getlist('checked_size_id'):
            size = Size.objects.get(article_size=article_size)
            baskets = Basket.objects.filter(user=request.user, product=product, size=size)
            if not baskets.exists():
                Basket.objects.create(user=request.user, product=product, qty=1, size=size)
            else:
                basket = baskets.last()
                basket.qty += 1
                basket.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
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
    Basket.objects.get(id=basket_id).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def remove_all_user_baskets(request):
    Basket.objects.filter(user=request.user).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def item_info(request, product_id):
    product = Product.objects.get(article=product_id)
    products = Product.objects.filter(model_group=product.model_group)
    context = {
        'title': "Информация о продукте",
        'product': product,
        'products': products,
    }
    return render(request, 'products/item_info.html', context)


class CartView(DataMixin, TemplateView):
    template_name = 'products/cart.html'
    title = "Корзина"


class FavoritesView(DataMixin, TemplateView):
    template_name = 'products/favorites.html'
    title = "Избранные товары"


def favorites_add(request, product_id):
    product = Product.objects.get(article=product_id)
    favorites = Favorites.objects.filter(user=request.user, product=product)
    if not favorites.exists():
        favorite = Favorites.objects.create(user=request.user, product=product, qty=1, is_favorite=True)
        favorite.save()
    else:
        favorite = Favorites.objects.get(product=product_id, user=request.user)
        favorite.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def favorites_remove(request, favorite_id):
    Favorites.objects.get(id=favorite_id, user=request.user).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def remove_all_user_favorites(request):
    Favorites.objects.filter(user=request.user).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
