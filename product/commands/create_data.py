import random
from django.core.management.base import BaseCommand
from faker import Faker
from product.models import Product, ProductCategory, ProductSubCategory, ProductBrands

fake = Faker()


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating fake data...'))
        categories = [ProductCategory.objects.create(name=fake.word(), id=fake.unique.random_int(
            min=111111, max=999999), slug=fake.slug()) for _ in range(5)]
        subcategories = [ProductSubCategory.objects.create(
            name=fake.word(), slug=fake.slug(), category_id=random.choice(categories).id) for _ in range(10)]
        brands = [ProductBrands.objects.create(
            name=fake.word(),  slug=fake.slug()) for _ in range(3)]
        for _ in range(10):
            product = Product.objects.create(
                name=fake.word(),
                description=fake.text(),
                slug=fake.slug(),
                price=random.uniform(10, 1000),
                image=fake.image_url(),
                category=random.choice(categories),
                subcategory=random.choice(subcategories),
                brand=random.choice(brands)
            )
            self.stdout.write(self.style.SUCCESS(
                f'Created product: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Fake data creation complete.'))
