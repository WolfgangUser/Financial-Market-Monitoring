from rest_framework import serializers
from .models import Asset, PriceData, Watchlist, MarketNews


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'symbol', 'name', 'asset_type', 'description', 'created_at', 'updated_at']


class PriceDataSerializer(serializers.ModelSerializer):
    asset_symbol = serializers.CharField(source='asset.symbol', read_only=True)
    
    class Meta:
        model = PriceData
        fields = ['id', 'asset', 'asset_symbol', 'timestamp', 'open_price', 'high_price', 
                  'low_price', 'close_price', 'volume']


class AssetWithPriceSerializer(serializers.ModelSerializer):
    current_price = serializers.SerializerMethodField()
    price_change = serializers.SerializerMethodField()
    
    class Meta:
        model = Asset
        fields = ['id', 'symbol', 'name', 'asset_type', 'current_price', 'price_change', 'description']
    
    def get_current_price(self, obj):
        latest_price = obj.prices.first()
        if latest_price:
            return float(latest_price.close_price)
        return None
    
    def get_price_change(self, obj):
        prices = obj.prices.all()[:2]
        if len(prices) >= 2:
            change = float(prices[0].close_price) - float(prices[1].close_price)
            percent = (change / float(prices[1].close_price)) * 100 if prices[1].close_price else 0
            return round(percent, 2)
        return None


class WatchlistSerializer(serializers.ModelSerializer):
    assets = AssetSerializer(many=True, read_only=True)
    asset_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Watchlist
        fields = ['id', 'name', 'assets', 'asset_count', 'created_at']
    
    def get_asset_count(self, obj):
        return obj.assets.count()


class MarketNewsSerializer(serializers.ModelSerializer):
    related_assets = AssetSerializer(many=True, read_only=True)
    
    class Meta:
        model = MarketNews
        fields = ['id', 'title', 'content', 'source', 'published_at', 'related_assets', 'created_at']
