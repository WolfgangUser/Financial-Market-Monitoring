from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
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
    
    # Получаем текущие цены и изменения для каждого актива
    assets_with_data = []
    for asset in assets:
        price_info = MarketDataService.get_current_price_with_change(asset)
        assets_with_data.append({
            'asset': asset,
            'current_price': price_info['current_price'],
            'change_percent': price_info['change_percent'],
            'previous_price': price_info['previous_price'],
        })
    
    return render(request, 'markets/home.html', {
        'assets_with_data': assets_with_data,
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


def login_view(request):
    """Страница входа пользователя"""
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    
    return render(request, 'markets/login.html', {'page_title': 'Вход'})


def register_view(request):
    """Страница регистрации пользователя"""
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Пароли не совпадают.')
            return render(request, 'markets/register.html', {'page_title': 'Регистрация'})
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Имя пользователя уже занято.')
            return render(request, 'markets/register.html', {'page_title': 'Регистрация'})
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, f'Аккаунт создан! Добро пожаловать, {user.username}!')
        return redirect('home')
    
    return render(request, 'markets/register.html', {'page_title': 'Регистрация'})


@login_required(login_url='login')
def profile_view(request):
    """Личный кабинет пользователя"""
    user_watchlists = Watchlist.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, 'markets/profile.html', {
        'page_title': 'Профиль',
        'watchlists': user_watchlists
    })


def logout_view(request):
    """Выход пользователя"""
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('home')


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
