from django.contrib import admin
from .models import Promo,Bde
# Register your models here.
admin.site.site_header = 'Recensement Admin Area'
@admin.register(Bde)
class BdeAdmin(admin.ModelAdmin):
    list_display = ('fullname',"promo")
    ordering = ("promo","fullname")
    search_fields = ("fullname","promo__level")

@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('level',"notion_token","page_id")
    ordering = ("level",)