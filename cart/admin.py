from django.contrib import admin
from cart.models import Cart ,WishList

@admin.register(Cart)
class cartAdmin(admin.ModelAdmin):
   list_display=['user','product','variation','quantity']
   list_filter=['user']
   search_fields=['user']
  
  
@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
   list_display=['user','product']
   list_filter=['user']
   search_fields=['user']
    