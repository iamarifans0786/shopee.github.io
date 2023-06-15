from django.contrib import admin, messages
from cms.models import (
    WebsiteSetting,
    Slider,
    Blog,
    FAQs,
    Testimonial,
    OurTeam,
    CustomerInquiry,
)


def active_status(modelAdmin, request, queryset):
    """Custom admin pannel actions for change blog status"""
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


def popular_slug_active_status(modelAdmin, request, queryset):
    """Custom admin pannel actions for change popular blog status"""
    try:
        queryset.update(popular_blog_status=True)
        messages.success(request, "Selected record(s) marked as active")
    except Exception as e:
        messages.error(request, str(e))


def popular_slug_inactive_status(modelAdmin, request, queryset):
    try:
        queryset.update(popular_blog_status=False)
        messages.success(request, "Selected record(s) marked as inactive")
    except Exception as e:
        messages.error(request, str(e))


@admin.register(WebsiteSetting)
class websiteSettingAdmin(admin.ModelAdmin):
    """Register Admin pannel for Website config like logo , title and contact detail"""

    list_display = ["title", "logo", "email", "phone", "address"]
    search_fields = ["title"]


@admin.register(Slider)
class sliderAdmin(admin.ModelAdmin):
    """Register Admin pannel for Dynamic slider for home page"""

    list_display = ["heading", "sub_heading", "image", "status"]
    list_filter = ["status"]
    search_fields = ["heading"]
    actions = (active_status, inactive_status)


@admin.register(Blog)
class blogAdmin(admin.ModelAdmin):
    """Register Admin pannel for Blog"""

    prepopulated_fields = {"slug": ("title",)}
    list_display = [
        "title",
        "sub_title",
        "description",
        "auther",
        "image",
        "popular_blog_status",
        "status",
    ]
    list_filter = ["status"]
    search_fields = ["title"]
    date_hierarchy = "date_time"
    actions = (
        active_status,
        inactive_status,
        popular_slug_active_status,
        popular_slug_inactive_status,
    )


@admin.register(FAQs)
class FAQsAdmin(admin.ModelAdmin):
    """Register Admin pannel for FAQs"""

    list_display = ["question", "answer", "status"]
    search_fields = ["question"]
    list_filter = ["status"]
    actions = (active_status, inactive_status)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Register Admin pannel for Tesliminial slider"""

    list_display = ["name", "comment", "image", "status"]
    search_fields = ["name"]
    list_filter = ["status"]
    actions = (active_status, inactive_status)


@admin.register(OurTeam)
class OurTeamAdmin(admin.ModelAdmin):
    """Register admin pannel for our team model for about page"""

    list_display = ["name", "position", "image", "status"]
    search_fields = ["name"]
    list_filter = ["status"]
    actions = (active_status, inactive_status)


@admin.register(CustomerInquiry)
class CustomerInquiryAdmin(admin.ModelAdmin):
    """Register admin pannel for our team model for about page"""

    list_display = ["name", "email", "phone", "message"]
    search_fields = ["name"]
    list_filter = ["name"]
