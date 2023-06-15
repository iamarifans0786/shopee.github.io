from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("contact/", views.contact_page, name="contact_page"),
    path("about/", views.about_page, name="about_page"),
    path("blog/", views.blog_page, name="blog_page"),
    path("blog-detail/<slug:blog_slug>", views.blog_detail, name="blog_detail"),
    path("FAQs/", views.FAQsView, name="FAQsView"),
    path("product/", views.product_page, name="product_page"),
    path(
        "product/<slug:product_category_slug>", views.product_page, name="product_page"
    ),
    path(
        "product-detail/<slug:product_slug>",
        views.product_detail,
        name="product_detail",
    ),
]
 