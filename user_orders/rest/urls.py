
from .views import OrderListCreate
from django.urls import path

urlpatterns = [
    path('order', OrderListCreate.as_view(), name="OrderListCreate"),

]
