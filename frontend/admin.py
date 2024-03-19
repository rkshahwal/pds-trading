from django.contrib import admin
from .models import *


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("id", "alt")
    list_filter = ("created_at", )


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('name', 'latest_price', 'fun_range', 'status', 'created_at')
    search_fields = ('name', )
    list_filter = ('status', 'created_at',)
