from django.contrib import admin, messages

from product.models import (
    Product,
    ProductCategory,
    ProductTags,
    ProductVariation,
    ProductImage,
)

""" for updation os ststus fields on admin pannel """


def active_status(modelAdmin, request, queryset):
    try:
        queryset.update(status=True)
        messages.success(request, "Selected record(s) marked as active")
    except Exception as e:
        messages.error(request, str(e))


def inactive_status(modelAdmin, request, queryset):
    try:
        queryset.update(status=False)
        messages.success(request, "Selected record(s) marked as inactive")
    except Exception as e:
        messages.error(request, str(e))

def flag_active_status(modelAdmin, request, queryset):
    try:
        queryset.update(show_homepage=True)
        messages.success(request, "Selected record(s) marked as active")
    except Exception as e:
        messages.error(request, str(e))


def flag_inactive_status(modelAdmin, request, queryset):
    try:
        queryset.update(show_homepage=False)
        messages.success(request, "Selected record(s) marked as inactive")
    except Exception as e:
        messages.error(request, str(e))

""" for display saprate table in product for multiple product image items  """


class ProductImageInline(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "cover_image", 
        "price",
        "description",
        "product_category",
        "show_homepage",
        "status",
    ]
    """ Slug genrate in run time we modifile also in run time """
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ["product_category"]
    search_fields = ["name"]
    actions = (active_status, inactive_status,flag_active_status,flag_inactive_status)
    inlines = (ProductImageInline,)


@admin.register(ProductCategory)
class productCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "image","show_homepage", "status"]
    list_filter = ["status"]
    search_fields = ["name"]
    actions = (active_status, inactive_status,flag_active_status,flag_inactive_status)
 

@admin.register(ProductVariation)
class productVariationAdmin(admin.ModelAdmin):
    list_display = ["name", "status"]
    list_filter = ["status"]
    search_fields = ["name"]
    actions = (active_status, inactive_status)


@admin.register(ProductTags)
class productTagsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "slug", "status"]
    list_filter = ["status"]
    search_fields = ["name"]
    actions = (active_status, inactive_status)


# @admin.register(productImage)
# class productImageAdmin(admin.ModelAdmin):
#     list_display = ["product", "image"]
#     list_filter = ["product"]
#     search_fields = ["product"]
