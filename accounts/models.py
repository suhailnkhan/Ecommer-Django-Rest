from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from phonenumber_field.modelfields import PhoneNumberField

from accounts.constants import ADMIN_ROLE,CUSTOMER_ROLE,SHOP_ADMIN_ROLE,SUPER_ADMIN_ROLE
from accounts.managers import UserManager
from accounts.permission_constants import BLINKBUY_ADMIN ,BLINKBUY_CUSTOMER , BLINKBUY_SHOP_ADMIN  , BLINKBUY_SUPER_ADMIN
from accounts.utils import salutation_choices


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    added_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
    modified_on = models.DateTimeField(auto_now=True, verbose_name="Last Modified on")

    class Meta:
        abstract = True



class User(AbstractUser, BaseModel):
    full_name = models.CharField(max_length=255)
    salutation = models.CharField(max_length=2, choices=salutation_choices(), default=salutation_choices()[0][0])
    email = models.EmailField(unique=True)
    mobile_number = PhoneNumberField(null=True, blank=True)
    # address = models.TextField(null = True , blank = True)
    profile_image = models.ImageField(upload_to='profile_images', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    class Meta:
        db_table = 'User'
        app_label = 'accounts'

    def save(self, *args, **kwargs):
        self.username = self.email
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        name = self.full_name
        return name + '<' + self.email + '>'

    def save_password(self, raw_password):
        if raw_password:
            self.set_password(raw_password)
            self.save()
        return self

    def label(self):
        name = self.full_name
        salutation = self.salutation
        if name and salutation:
            name = salutation + ' ' + name
        elif not name:
            name = self.username
        return name

    @property
    def number(self):
        number = str()
        if self.mobile_number:
            try:
                number = self.mobile_number.as_e164
            except:
                pass
        return number

    @property
    def permissions(self):
        return self.user_permissions.all()

    def has_permission(self, codename):
        return User.objects.has_permission(user=self, codename=codename)

    def get_permission(self, codename):
        return User.objects.get_permission(user=self, codename=codename)

    @property
    def is_super_admin(self):
        if self.has_permission(codename=BLINKBUY_SUPER_ADMIN) or self.is_superuser:
            return True
        return False

    @property
    def is_admin(self):
        return self.has_permission(codename=BLINKBUY_ADMIN)
    @property
    def is_super_admin(self):
        return self.has_permission(codename=BLINKBUY_SUPER_ADMIN)   
    @property
    def is_customer(self):
        return self.has_permission(codename=BLINKBUY_CUSTOMER)

    @property
    def is_shop_admin(self):
        return self.has_permission(codename=BLINKBUY_SHOP_ADMIN)

    @property
    def role(self):
        role = str()
        if self.is_admin:
            role = ADMIN_ROLE
        elif self.is_customer:
            role = CUSTOMER_ROLE
        elif self.shop_admin:
            role = SHOP_ADMIN_ROLE
        elif self.is_super_admin:
            role = SUPER_ADMIN_ROLE
        return role

    @property
    def customer(self):
        if self.is_customer:
            return self.customer_set.all().first()
        return None

    @property
    def shop_admin(self):
        if self.is_shop_admin:
            return self.shop_admin_set.all().first()
        return None

   


