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
    """Главная страница"""
    assets = Asset.objects.all()[:10]
    news = NewsService.get_latest_news(5)
    return render(request, 'markets/home.html', {
        'assets': assets,
        'news': news,
        'page_title': 'Панель управления'
    })


def assets_list_view(request):
    """Список всех активов"""
    asset_type = request.GET.get('type', '')
    if asset_type:
        assets = Asset.objects.filter(asset_type=asset_type)
    else:
        assets = Asset.objects.all()
    
    return render(request, 'markets/assets.html', {
        'assets': assets,
        'page_title': 'Активы',
        'current_type': asset_type
    })


def asset_detail_view(request, symbol):
    """Детальная информация об активе"""
    asset = get_object_or_404(Asset, symbol=symbol)
    prices = PriceData.objects.filter(asset=asset)[:30]
    historical_data = MarketDataService.fetch_historical_data(asset, 30)
    
    return render(request, 'markets/asset_detail.html', {
        'asset': asset,
        'prices': prices,
        'historical_data': historical_data,
        'page_title': f'{asset.symbol} - Детали'
    })


def news_view(request):
    """Страница новостей рынка"""
    news_items = NewsService.get_latest_news(20)
    return render(request, 'markets/news.html', {
        'news_items': news_items,
        'page_title': 'Новости рынка'
    })


def watchlists_view(request):
    """Страница списков наблюдения"""
    watchlists = Watchlist.objects.prefetch_related('assets').all()
    return render(request, 'markets/watchlists.html', {
        'watchlists': watchlists,
        'page_title': 'Списки наблюдения'
    })


# ==================== REST API Views (DRF) ====================

class AssetViewSet(viewsets.ModelViewSet):
    """API endpoint для активов"""
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AssetWithPriceSerializer
        return AssetSerializer


class PriceDataViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint для данных о ценах"""
    queryset = PriceData.objects.all().order_by('-timestamp')
    serializer_class = PriceDataSerializer


class WatchlistViewSet(viewsets.ModelViewSet):
    """API endpoint для списков наблюдения"""
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer


class MarketNewsViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint для новостей рынка"""
    queryset = MarketNews.objects.all()
    serializer_class = MarketNewsSerializer


class AssetPriceView(APIView):
    """Получить текущую цену актива"""
    
    def get(self, request, symbol):
        asset = get_object_or_404(Asset, symbol=symbol)
        price_data = MarketDataService.get_asset_price(symbol)
        
        if price_data:
            # Обновить базу данных
            MarketDataService.update_asset_prices(asset)
            return Response(price_data)
        
        return Response({'error': 'Данные о цене недоступны'}, status=status.HTTP_404_NOT_FOUND)


class MarketOverviewView(APIView):
    """Получить обзор рынка с лидерами роста/падения"""
    
    def get(self, request):
        assets = Asset.objects.all()[:20]
        serializer = AssetWithPriceSerializer(assets, many=True)
        
        # Рассчитать статистику рынка
        total_assets = Asset.objects.count()
        total_price_records = PriceData.objects.count()
        
        return Response({
            'assets': serializer.data,
            'stats': {
                'total_assets': total_assets,
                'total_price_records': total_price_records,
            }
        })
