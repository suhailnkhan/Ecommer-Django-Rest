
from .views import CartListCreate, AddToCartView, RemoveCartItem
from django.urls import path

urlpatterns = [
    path('cart', CartListCreate.as_view(), name="cartListCreate"),
    path('add-to-cart/', AddToCartView.as_view(), name="AddToCartView"),
    path('delete-cart-item/<int:pk>', RemoveCartItem.as_view(), name="DeleteCart")
]
