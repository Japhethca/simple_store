from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model

User = get_user_model()


class SettingsBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        login_valid = settings.ADMIN_LOGIN == username
        pass_valid = check_password(password, settings.ADMIN_PASSWORD)
        if login_valid and pass_valid:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                # user does not exist
                user = User(email=username)
                user.is_admin = True
                user.save()
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def has_perm(self, user_obj, perm, obj=None):
        return user_obj.email == settings.ADMIN_LOGIN
