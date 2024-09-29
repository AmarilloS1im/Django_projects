from django.contrib.auth.decorators import login_required
from django.urls import path

from products.views import (CartView, FavoritesView, basket_add, basket_remove,
                            cart_add_plus_one, cart_del_minus_one,
                            favorites_add, favorites_remove, item_info,
                            products, remove_all_user_baskets,
                            remove_all_user_favorites, reset_filters)
from django.views.decorators.cache import cache_page

app_name = 'products'
urlpatterns = [
    path('', login_required(products), name='products'),
    path('page/<int:page>/', login_required(products), name='paginator'),
    path('reset/', login_required(reset_filters), name='reset_filters'),
    path('item_info/<str:product_id>', login_required(item_info), name='item_info'),
    path('baskets/add/<str:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>', basket_remove, name='basket_remove'),
    path('cart/', login_required(CartView.as_view()), name='cart'),
    path('baskets/remove/', remove_all_user_baskets, name='remove_all_user_baskets'),
    path('cart/add/<int:basket_id>/', cart_add_plus_one, name='cart_add_plus_one'),
    path('cart/del/<int:basket_id>', cart_del_minus_one, name='cart_del_minus_one'),
    path('favorites/add/<str:product_id>', login_required(favorites_add), name='favorites_add'),
    path('favorites/', login_required(FavoritesView.as_view()), name='favorites'),
    path('favorites/remove/<int:favorite_id>/', favorites_remove, name='favorites_remove'),
    path('favorites/remove/', remove_all_user_favorites, name='remove_all_user_favorites'),
]
