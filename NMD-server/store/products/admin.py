from django.contrib import admin
from products.models import (Product, Size, Basket, Favorites,
                             ProductCategory, ProductType, ProductGender, ProductAge, ProductSeason)


admin.site.register(Product)
admin.site.register(Size)
admin.site.register(Basket)
admin.site.register(Favorites)
admin.site.register(ProductCategory)
admin.site.register(ProductType)
admin.site.register(ProductGender)
admin.site.register(ProductAge)
admin.site.register(ProductSeason)
