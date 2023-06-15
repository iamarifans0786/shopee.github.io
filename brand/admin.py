from django.contrib import admin,messages
from brand.models import Brand

def active_status(modelAdmin,request,queryset):
   try: 
      queryset.update(status=True)
      messages.success(request,'Selected record(s) marked as active')
   except Exception as e:
      messages.error(request,str(e))
      
def inactive_status(modelAdmin,request,queryset):
   try:
      queryset.update(status=False)
      messages.success(request,'Selected record(s) marked as inactive')
   except Exception as e:
      messages.error(request,str(e))


@admin.register(Brand)
class brandAdmin(admin.ModelAdmin):
   list_display=['name','status']
   list_filter=['status']
   search_fields=['name']
   actions=(active_status, inactive_status)