from product.models import Product, ProductSubCategory, ProductCategory, ProductBrands
from rest_framework import serializers


class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_brand(self, obj):
        if obj.brand:
            return {"name": obj.brand.name, "id": obj.brand.id}
        return str()

    def get_category(self, obj):
        if obj.category:
            return {"name": obj.category.name, "id": obj.category.id}
        return str()

    def get_subcategory(self, obj):
        if obj.subcategory:
            return {"name": obj.subcategory.name, "id": obj.subcategory.id}
        return str()


class ProductSubCategorySerializer(serializers.ModelSerializer):
    parent_category_name = serializers.SerializerMethodField()

    class Meta:
        model = ProductSubCategory
        fields = "__all__"

    def get_parent_category_name(self, obj):
        if obj.category:
            return obj.category.name
        return str()


class ProductCategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'slug', 'image', 'sub_categories']

    def get_sub_categories(self, obj):
        sub_categories = ProductSubCategory.objects.filter(category=obj.id)
        serialized_sub_categories = ProductSubCategorySerializer(
            sub_categories, many=True).data
        return serialized_sub_categories


class ProductBrandSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductBrands
        fields = ['id', 'image']

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None
