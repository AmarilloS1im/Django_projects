from django.db import models
from users.models import User


class Product(models.Model):
    article = models.CharField(max_length=12, null=False, blank=False, unique=True, primary_key=True)
    model_name = models.CharField(max_length=12, null=False, blank=False)
    model_group = models.CharField(max_length=12, null=False, blank=False)
    img = models.ImageField(upload_to='products_images')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=24, null=False)
    sizes = models.ForeignKey(to='Size', on_delete=models.CASCADE, to_field='article_size')
    category = models.ForeignKey(to='ProductCategory', on_delete=models.PROTECT, to_field='name')
    product_type = models.ForeignKey(to='ProductType', on_delete=models.PROTECT, to_field='name')
    gender = models.ForeignKey(to='ProductGender', on_delete=models.PROTECT, to_field='name')
    season = models.ForeignKey(to='ProductSeason', on_delete=models.PROTECT, to_field='name')
    age = models.ForeignKey(to='ProductAge', on_delete=models.PROTECT, to_field='name')

    def __str__(self):
        return f"{self.article}"


class ProductAge(models.Model):
    name = models.CharField(max_length=12, null=False, unique=True, primary_key=True)
    userfrendly_name = models.TextField(null=True, blank=True)


class ProductSeason(models.Model):
    name = models.CharField(max_length=12, null=False, unique=True, primary_key=True)
    userfrendly_name = models.TextField(null=True, blank=True)


class ProductGender(models.Model):
    name = models.CharField(max_length=12, null=False, unique=True, primary_key=True)
    userfrendly_name = models.TextField(null=True, blank=True)


class ProductCategory(models.Model):
    name = models.CharField(max_length=12, null=False, unique=True, primary_key=True)
    userfrendly_name = models.TextField(null=True, blank=True)


class ProductType(models.Model):
    name = models.CharField(max_length=12, null=False, unique=True, primary_key=True)
    userfrendly_name = models.TextField(null=True, blank=True)


class Size(models.Model):
    article_size = models.CharField(max_length=12, null=False, unique=True, primary_key=True)
    size_name = models.CharField(max_length=12, null=False, blank=False)
    qty = models.SmallIntegerField()
    to_article = models.CharField(max_length=12, null=False)

    def __str__(self):
        return f"{self.article_size}"


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_qty(self):
        return sum(basket.qty for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, to_field='article')
    size = models.ForeignKey(to=Size, on_delete=models.PROTECT, to_field='article_size')
    qty = models.PositiveSmallIntegerField(default=0)
    create_time_stamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Корзина для {self.user.email} товар {self.product.article},размер {self.size.size_name}"

    def sum(self):
        return self.product.price * self.qty


class FavoritesQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(favorites.sum() for favorites in self)

    def total_qty(self):
        return sum(favorites.qty for favorites in self)


class Favorites(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, to_field='article')
    qty = models.PositiveSmallIntegerField(default=0)
    create_time_stamp = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(null=False, default=False, blank=False)
    objects = FavoritesQuerySet.as_manager()

    def __str__(self):
        return f"Избранные товары для {self.user.email} товар {self.product.article}"

    def sum(self):
        return self.product.price * self.qty


class SizeSelected(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    create_time_stamp = models.DateTimeField(auto_now_add=True)
    is_selected = models.BooleanField(null=False, default=True, blank=False)
