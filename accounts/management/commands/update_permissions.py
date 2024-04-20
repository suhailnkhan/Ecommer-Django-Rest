from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from accounts.models import User
from accounts.permission_constants import BLINKBUY_USER_ROLES


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_content_type = ContentType.objects.get_for_model(User)
        for codename, name in BLINKBUY_USER_ROLES.items():
            perm, created = Permission.objects.get_or_create(content_type=user_content_type, codename=codename)
            perm.name = name
            perm.save()