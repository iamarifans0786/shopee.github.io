from cms.models import WebsiteSetting

""" Context processor for dynamic title,logo and address """
def website_config(request):
    website_setting = WebsiteSetting.objects.all().last()
    return {"website_setting": website_setting}
