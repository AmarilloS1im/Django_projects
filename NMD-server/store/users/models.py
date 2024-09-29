from django.contrib.auth.models import AbstractUser, UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

from django.db import models
from image_cropping import ImageRatioField

from PIL import Image
from django.db import models
from image_cropping import ImageCropField, ImageRatioField


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        null=True,
        blank=True,
    )
    email = models.EmailField(_("email address"), unique=True)
    # image = models.ImageField(upload_to='users_images', blank=True, null=True)
    image = ImageCropField(blank=True, upload_to='users_images', null= True)
    cropping = ImageRatioField('image', '180x180')

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    # def save(self):
    #     super().save()  # saving image first
    #     img = Image.open(self.image.path) # Open image using self
    #     print(img.height)
    #     print(img.width)
    #     percent_ratio= 0.1
    #
    #
    #     if img.height > 180 or img.width > 180:
    #         new_img = (174,171)
    #         print(new_img)
    #
    #         img.thumbnail(new_img)
    #         img.save(self.image.path)
