from product.models import ProductCategory


def navigation_categories_config(request):
    """Context processor for dynamic product category in header"""
    navigation_categories = ProductCategory.objects.filter(status=True)
    return {"navigation_categories": navigation_categories}
