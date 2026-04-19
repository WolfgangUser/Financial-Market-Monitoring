from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'assets', views.AssetViewSet)
router.register(r'prices', views.PriceDataViewSet)
router.register(r'watchlists', views.WatchlistViewSet)
router.register(r'news', views.MarketNewsViewSet)

urlpatterns = [
    # Web pages (MVC Views)
    path('', views.home_view, name='home'),
    path('assets/', views.assets_list_view, name='assets-list'),
    path('assets/<str:symbol>/', views.asset_detail_view, name='asset-detail'),
    path('news/', views.news_view, name='news'),
    path('watchlists/', views.watchlists_view, name='watchlists'),
    
    # REST API
    path('api/', include(router.urls)),
    path('api/asset/<str:symbol>/price/', views.AssetPriceView.as_view(), name='asset-price'),
    path('api/market-overview/', views.MarketOverviewView.as_view(), name='market-overview'),
]
