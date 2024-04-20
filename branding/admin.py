from django.contrib import admin

# Register your models here.
from .models import HeroBrand, FeaturedBanner

admin.site.register(HeroBrand)
admin.site.register(FeaturedBanner)
