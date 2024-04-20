from django.db import models
import uuid


class BaseModel(models.Model):
    added_on = models.DateTimeField(
        auto_now_add=True, verbose_name="Created On")
    modified_on = models.DateTimeField(
        auto_now=True, verbose_name="Last Modified on")

    class Meta:
        abstract = True


class ProductBrands(BaseModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='products/brands/')
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name


class ProductCategory(BaseModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(
        upload_to='products/category', null=True, blank=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name


class ProductSubCategory(BaseModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/sub-category')
    slug = models.SlugField(unique=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.category} - {self.name}"


class Product(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(
        ProductSubCategory, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(
        ProductBrands, on_delete=models.CASCADE, null=True, blank=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name
