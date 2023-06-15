from django.contrib import admin
from user_profile.models import UserProfile

@admin.register(UserProfile)
class userProfile(admin.ModelAdmin):
    list_display = ["user","mobile","address","profile_image"]
    list_filter = ["mobile"]
    search_fields = ["mobile"]
 