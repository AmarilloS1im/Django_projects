from django.contrib import admin
from django.contrib import admin
from image_cropping import ImageCroppingMixin

from .models import User

class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass

admin.site.register(User,MyModelAdmin)
