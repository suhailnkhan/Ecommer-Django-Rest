from django.db import models
from user_orders.models import Order
from .constant import STATUS_CHOICES, STATUS_COMPLETED, PAYMENT_TYPES_CASH_ON_DELIVERY
from accounts.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_COMPLETED)
    mode = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default=PAYMENT_TYPES_CASH_ON_DELIVERY)
    id = models.AutoField(primary_key=True)

@receiver(post_save, sender=Order)
def create_payment(sender, instance, created, **kwargs):
    if created:
        Payment.objects.create(user=instance.user, order=instance, amount=instance.total_amount,
                               mode=PAYMENT_TYPES_CASH_ON_DELIVERY,  status=STATUS_COMPLETED)
