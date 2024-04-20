from product.service import get_thumbnail_url


class ProductsManager:
    @staticmethod
    def get_products_with_details(query_set, request):
        products = []
        for product in query_set:
            product_data = {
                'id': product.id,
                'slug': product.slug,
                'name': product.name,
                "size": None,
                "brand": product.brand.id,
                "price": product.price,
                "sale_price": product.price,
                "description": product.description,
                "variations": [],
                "image": {
                    "id": 1,
                    "thumbnail":  get_thumbnail_url(request, product.image),
                    "original":  get_thumbnail_url(request, product.image),
                },
                "categories": product.category.id,
                "status": None,
                "reviews": [],
                "rating": 0,
            }
            products.append(product_data)
        return products


class ProductManager:
    @staticmethod
    def get_product_with_details(instance, request):
        product_data = {
            'id': instance.id,
            'slug': instance.slug,
            'name': instance.name,
            "size": None,
            "brand": instance.brand.id,
            "price": instance.price,
            "sale_price": instance.price,
            "description": instance.description,
            "variations": [],
            "image": {
                "id": 1,
                "thumbnail":  get_thumbnail_url(request, instance.image),
                "original":  get_thumbnail_url(request, instance.image),
            },
            "categories": instance.category.id,
            "status": None,
            "reviews": [],
            "rating": 0,
        }
        return product_data
