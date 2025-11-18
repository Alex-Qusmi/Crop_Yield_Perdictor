# dashboard/admin.py
from django.contrib import admin
from .models import MarketPrice, FeaturedCrop

@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ('crop', 'variety', 'price', 'mandi', 'trend', 'last_updated')
    list_filter = ('mandi', 'crop', 'trend')
    search_fields = ('crop', 'variety', 'mandi')

@admin.register(FeaturedCrop)
class FeaturedCropAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag', 'district')
    list_filter = ('district', 'tag')
    search_fields = ('name',)