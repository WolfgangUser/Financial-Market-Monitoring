from django.contrib import admin
from .models import Asset, PriceData, Watchlist, MarketNews


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'name', 'asset_type', 'created_at', 'updated_at']
    list_filter = ['asset_type', 'created_at']
    search_fields = ['symbol', 'name', 'description']
    ordering = ['symbol']


@admin.register(PriceData)
class PriceDataAdmin(admin.ModelAdmin):
    list_display = ['asset', 'close_price', 'timestamp', 'volume']
    list_filter = ['asset', 'timestamp']
    search_fields = ['asset__symbol']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    filter_horizontal = ['assets']
    search_fields = ['name']


@admin.register(MarketNews)
class MarketNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'published_at', 'created_at']
    list_filter = ['source', 'published_at']
    search_fields = ['title', 'content']
    date_hierarchy = 'published_at'
    filter_horizontal = ['related_assets']
