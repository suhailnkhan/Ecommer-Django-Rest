# from .views import
from django.urls import path
from .views import CreateListHeroBrand, CreateListFeaturedBanner
urlpatterns = [
    path('hero-brand/', CreateListHeroBrand.as_view(),
         name='sub_categories_listing_creation'),
    path("feature-banner/", CreateListFeaturedBanner.as_view(),
         name='feature_banner')
]
