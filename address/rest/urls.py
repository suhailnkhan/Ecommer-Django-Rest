
from .views import AddressListCreate
from django.urls import path

urlpatterns = [
    path('address/', AddressListCreate.as_view(), name="AddressListCreate"),

]
