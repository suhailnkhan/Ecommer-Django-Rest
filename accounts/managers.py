from django.contrib.auth.models import UserManager
from django.contrib.auth.models import Permission


class UserManager(UserManager):
    def not_deleted(self):
        return self.get_queryset().filter(is_deleted=False)

    def has_permission(self, user, codename):
        user_perm = Permission.objects.filter(codename=codename).first()
        if user_perm and user_perm in user.permissions:
            return True
        return False

    def get_permission(self, user, codename):
        user_perm = Permission.objects.filter(codename=codename).first()
        if user_perm and user_perm in user.permissions:
            return user_perm
        return False
