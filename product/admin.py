from django.contrib import admin

# Register your models here.

from .models import Product, ProductCategory, ProductSubCategory, ProductBrands

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductSubCategory)
admin.site.register(ProductBrands)
