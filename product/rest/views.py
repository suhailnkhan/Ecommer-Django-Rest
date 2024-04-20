from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from product.rest.serializers import ProductListSerializer, ProductCategory, ProductCategorySerializer, ProductSubCategorySerializer, ProductBrandSerializer
from product.models import Product, ProductCategory, ProductSubCategory, ProductBrands
from rest_framework.status import *
from product.service import get_thumbnail_url
from product.manager import ProductsManager, ProductManager


class ProductListAPIView(ListCreateAPIView):
    serializer_class = ProductListSerializer
    # queryset = Product.objects.all()

    def get_queryset(self):
        products = Product.objects.all()
        return products

    def get(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        products_data = ProductsManager.get_products_with_details(
            query_set, request)
        return Response({'data': products_data})


class CreateListProductCategoryView(ListCreateAPIView):
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()

    def sub_categories(self, id):
        sub_category = []
        sub_categories = ProductSubCategory.objects.filter(category=id)
        for c in sub_categories:
            sub_category.append({
                "label": c.name,
                "path": f"/product/search/{c.slug}",
                'slug': c.slug,
                'id': c.id,
                "icon": 'Dress',
            })
        return sub_category

    def get(self, request, *args, **kwargs):
        categories = []
        for q in self.queryset.all():
            tempDict = {
                'id': q.id,
                "label": q.name,
                "path": q.slug,
                "subMenu": self.sub_categories(q.id),
                "menuComponent": "MegaMenu2",
                "image": get_thumbnail_url(self, q.image),
                "slug": q.slug

            }
            categories.append(tempDict)
        return Response({"data": categories})


class CreateListProductSubCategoryView(ListCreateAPIView):
    queryset = ProductSubCategory.objects.all()
    serializer_class = ProductSubCategorySerializer


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    def get_serializer_class(self):
        return ProductListSerializer

    def get_queryset(self):
        return Product.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print("instance", instance)
        products_data = ProductManager.get_product_with_details(
            instance, request)
        return Response({'data': products_data})


class ProductBrandsListCreate(ListCreateAPIView):
    queryset = ProductBrands.objects.all()
    serializer_class = ProductBrandSerializer

    def get(self, request, *args, **kwargs):
        product_brands = self.get_queryset()
        serializer = self.serializer_class(product_brands, many=True)
        return Response({'data': serializer.data})

    def get(self, request, *args, **kwargs):
        data = []
        for q in self.queryset.all():
            tempDict = {
                "id": q.id,
                "image": get_thumbnail_url(self, q.image),
            }
        data.append(tempDict)
        return Response({"data": data})


class ListCategoryLinkedProducts(ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        products = Product.objects.filter(category_id=category_id)
        return products

    def get(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        products_data = ProductsManager.get_products_with_details(
            query_set, request)
        return Response({'data': products_data})
