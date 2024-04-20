from django.urls import path
from product.rest.views import ProductListAPIView
from product.rest.views import ListCategoryLinkedProducts
from product.rest.views import CreateListProductCategoryView
from product.rest.views import CreateListProductSubCategoryView
from product.rest.views import ProductRetrieveUpdateDestroyAPIView
from product.rest.views import ProductBrandsListCreate
urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='products_listing'),
    path('categories/', CreateListProductCategoryView.as_view(),
         name='categories_listing_creation'),
    path('sub-categories/', CreateListProductSubCategoryView.as_view(),
         name='sub_categories_listing_creation'),
    path('products/<int:pk>', ProductRetrieveUpdateDestroyAPIView.as_view(),
         name='products_listing'),
    path("product-brands", ProductBrandsListCreate.as_view(),
         name="product_brands_listing"),
    path('category-products/<int:pk>/', ListCategoryLinkedProducts.as_view(),
         name="category_products_listing"),
]
