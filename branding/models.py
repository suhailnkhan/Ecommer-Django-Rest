from django.db import models

# Create your models here.


class BaseModel(models.Model):
    added_on = models.DateTimeField(
        auto_now_add=True, verbose_name="Created On")
    modified_on = models.DateTimeField(
        auto_now=True, verbose_name="Last Modified on")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='brands/images')
    link = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True


class HeroBrand(BaseModel):
    buttonText = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


class FeaturedBanner(BaseModel):
    sub_title = models.CharField(max_length=100)
