from django.contrib.auth.backends import BaseBackend
from users.models import User


class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        user_model = User
        try:
            user = user_model.objects.get(email=email)
            if user.check_password(password):
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None
