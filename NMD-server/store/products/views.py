from django.shortcuts import render, HttpResponse, HttpResponseRedirect,redirect
from products.models import *
from products.forms import CheckboxForm
from products.context_processors import *
from django.shortcuts import render
from django.core.paginator import Paginator





# Create your views here.





def reset_filters(request):
    print('reset')
    request.session['filters']=[]
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def products(request,page=1):
    filter_dict={'category__in':['Shoe','Clothes'],'product_type__in':
        ['Boots','Longboots','Short_boots','Pullover','Sneakers'],
        'gender__in': ['Male', 'Female'],'season__in':['Winter','Summer'],'age__in':['Adult','Child'],
        }



    filters = request.POST.getlist('filter_id')
    print(filters)
    if len(filters)>0:
        filter_param_list = []
        for items in filters:
            for k,v in filter_dict.items():
                if items in filter_dict[k]:
                    filter_param_list.append(k)
                    break
    else:
        if request.session['filters']:
            filter_param_list = []
            for items in request.session['filters']:
                for k, v in filter_dict.items():
                    if items in filter_dict[k]:
                        filter_param_list.append(k)
                        break
        else:
            pass


    if len(filters)> 0:
        request.session['filters'] = filters
        current_filters = request.session['filters']
        param_dict = {}
        for param_name in filter_param_list:
            param_dict[param_name]=current_filters
        products = Product.objects.filter(**param_dict).order_by('article')
    else:
        if request.session['filters']:
            current_filters = request.session['filters']
            param_dict = {}
            for param_name in filter_param_list:
                param_dict[param_name] = current_filters
            products = Product.objects.filter(**param_dict).order_by('article')
        else:
            products = Product.objects.all().order_by('article')
    baskets = Basket.objects.filter(user=request.user)
    favorites = Favorites.objects.filter(user=request.user).order_by('product')

    paginator = Paginator(products,per_page=3)
    products_paginator = paginator.page(page)
    context = {
        'title': "Магазин",
        'footer_1': "127015, Москва, Бумажный пр-д., д. 14, стр. 2 ООО «НИКАМЕД».",
        'footer_2': "Копирование материалов запрещено.",
        'products': products_paginator,
        'sizes': Size.objects.all(),
        'baskets': baskets,
        'favorites': favorites,
        'categories': ProductCategory.objects.all(),
        'product_types': ProductType.objects.all(),
        'genders': ProductGender.objects.all(),
        'ages': ProductAge.objects.all(),
        'seasons': ProductSeason.objects.all(),
    }

    return render(request, 'products/products.html', context)





def basket_add(request, product_id):
    product = Product.objects.get(article=product_id)

    if request.method == 'POST':
        print('post')
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
        print('not post')
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
    products = Product.objects.filter(model_group=product.model_group)
    baskets = Basket.objects.filter(user=request.user)
    favorites = Favorites.objects.filter(user=request.user).order_by('product')
    context = {
        'title': "Магазин",
        'footer_1': "127015, Москва, Бумажный пр-д., д. 14, стр. 2 ООО «НИКАМЕД».",
        'footer_2': "Копирование материалов запрещено.",
        'product': product,
        'products': products,
        'sizes': Size.objects.all(),
        'baskets': baskets,
        'favorites': favorites,

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

    return render(request, 'products/favorites.html', context)


def favorites_add(request, product_id):
    product = Product.objects.get(article=product_id)
    favorites = Favorites.objects.filter(user=request.user, product=product)
    if not favorites.exists():
        favorite = Favorites.objects.create( user=request.user, product=product, qty=1, is_favorite=True)
        favorite.save()
    else:
        favorite = Favorites.objects.get(product=product_id,user=request.user)
        favorite.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def favorites_remove(request, favorite_id):
    favorite = Favorites.objects.get(id=favorite_id,user=request.user)
    favorite.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def remove_all_user_favorites(request):
    all_user_favorites = Favorites.objects.filter(user=request.user)
    all_user_favorites.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])












