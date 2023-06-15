from django.db import models
from django.template.defaultfilters import slugify
from brand.models import Brand

""" Modle for product class """


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="product_category")
    status = models.BooleanField(default=True)
    show_homepage = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductCategory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Product Categorie"


class ProductVariation(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProductTags(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductTags, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Product Tag"


class Product(models.Model):
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_name="product_category"
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,related_name="product_brand")
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    cover_image = models.ImageField(upload_to="products")
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField()
    variation = models.ManyToManyField(ProductVariation, related_name="product_variations")
    tags = models.ManyToManyField(ProductTags,related_name="product_tags")
    stock = models.IntegerField(default=1)
    status = models.BooleanField(default=True)
    show_homepage = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images"
    )
    image = models.ImageField(upload_to="products")

    def __str__(self):
        return str(self.id)
