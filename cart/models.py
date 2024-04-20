from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from product.models import Product
from accounts.models import User
import uuid
from user_orders.models import Order


class BaseModel(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    added_on = models.DateTimeField(
        auto_now_add=True, verbose_name="Created On")
    modified_on = models.DateTimeField(
        auto_now=True, verbose_name="Last Modified on")

    class Meta:
        abstract = True


class Cart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem')
    id = models.AutoField(primary_key=True)


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in {self.cart.user.username}\'s cart'

# Create a cart for each new user


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(post_save, sender=Order)
def clear_cart_items(sender, instance, created, **kwargs):
    try:
        cart = Cart.objects.get(user=instance.user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_items.delete()
    except Cart.DoesNotExist:
        pass  
