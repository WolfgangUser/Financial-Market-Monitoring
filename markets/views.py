from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Asset, PriceData, Watchlist, MarketNews
from .serializers import (
    AssetSerializer, AssetWithPriceSerializer, PriceDataSerializer,
    WatchlistSerializer, MarketNewsSerializer
)
from .services import MarketDataService, NewsService


# ==================== MVC Pattern: Views (Controller Layer) ====================

def home_view(request):
    """Home page view"""
    assets = Asset.objects.all()[:10]
    news = NewsService.get_latest_news(5)
    return render(request, 'markets/home.html', {
        'assets': assets,
        'news': news,
        'page_title': 'Dashboard'
    })


def assets_list_view(request):
    """List all assets"""
    asset_type = request.GET.get('type', '')
    if asset_type:
        assets = Asset.objects.filter(asset_type=asset_type)
    else:
        assets = Asset.objects.all()
    
    return render(request, 'markets/assets.html', {
        'assets': assets,
        'page_title': 'Assets',
        'current_type': asset_type
    })


def asset_detail_view(request, symbol):
    """Detail view for a single asset"""
    asset = get_object_or_404(Asset, symbol=symbol)
    prices = PriceData.objects.filter(asset=asset)[:30]
    historical_data = MarketDataService.fetch_historical_data(asset, 30)
    
    return render(request, 'markets/asset_detail.html', {
        'asset': asset,
        'prices': prices,
        'historical_data': historical_data,
        'page_title': f'{asset.symbol} - Details'
    })


def news_view(request):
    """Market news page"""
    news_items = NewsService.get_latest_news(20)
    return render(request, 'markets/news.html', {
        'news_items': news_items,
        'page_title': 'Market News'
    })


def watchlists_view(request):
    """Watchlists page"""
    watchlists = Watchlist.objects.prefetch_related('assets').all()
    return render(request, 'markets/watchlists.html', {
        'watchlists': watchlists,
        'page_title': 'Watchlists'
    })


# ==================== REST API Views (DRF) ====================

class AssetViewSet(viewsets.ModelViewSet):
    """API endpoint for assets"""
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AssetWithPriceSerializer
        return AssetSerializer


class PriceDataViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for price data"""
    queryset = PriceData.objects.all().order_by('-timestamp')
    serializer_class = PriceDataSerializer


class WatchlistViewSet(viewsets.ModelViewSet):
    """API endpoint for watchlists"""
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer


class MarketNewsViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for market news"""
    queryset = MarketNews.objects.all()
    serializer_class = MarketNewsSerializer


class AssetPriceView(APIView):
    """Get current price for an asset"""
    
    def get(self, request, symbol):
        asset = get_object_or_404(Asset, symbol=symbol)
        price_data = MarketDataService.get_asset_price(symbol)
        
        if price_data:
            # Update database
            MarketDataService.update_asset_prices(asset)
            return Response(price_data)
        
        return Response({'error': 'Price data not available'}, status=status.HTTP_404_NOT_FOUND)


class MarketOverviewView(APIView):
    """Get market overview with top movers"""
    
    def get(self, request):
        assets = Asset.objects.all()[:20]
        serializer = AssetWithPriceSerializer(assets, many=True)
        
        # Calculate market stats
        total_assets = Asset.objects.count()
        total_price_records = PriceData.objects.count()
        
        return Response({
            'assets': serializer.data,
            'stats': {
                'total_assets': total_assets,
                'total_price_records': total_price_records,
            }
        })
