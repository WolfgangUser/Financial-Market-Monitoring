import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_monitor.settings')
django.setup()

from markets.models import Asset, Watchlist, MarketNews
from markets.services import MarketDataService, NewsService
from django.utils import timezone
from datetime import timedelta

# Демо-данные активов
assets_data = [
    {'symbol': 'AAPL', 'name': 'Apple Inc.', 'asset_type': 'STOCK', 'description': 'Технологическая компания, разрабатывающая и производящая потребительскую электронику.'},
    {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'asset_type': 'STOCK', 'description': 'Многонациональная технологическая холдинговая компания.'},
    {'symbol': 'MSFT', 'name': 'Microsoft Corporation', 'asset_type': 'STOCK', 'description': 'Технологическая корпорация, производящая компьютерное программное обеспечение и потребительскую электронику.'},
    {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'asset_type': 'STOCK', 'description': 'Компания по производству электромобилей и чистой энергии.'},
    {'symbol': 'BTC', 'name': 'Bitcoin', 'asset_type': 'CRYPTO', 'description': 'Децентрализованная цифровая криптовалюта.'},
    {'symbol': 'ETH', 'name': 'Ethereum', 'asset_type': 'CRYPTO', 'description': 'Платформа блокчейн с открытым исходным кодом с функциональностью смарт-контрактов.'},
    {'symbol': 'EURUSD', 'name': 'Евро / Доллар США', 'asset_type': 'FOREX', 'description': 'Валютная пара, представляющая евро к доллару США.'},
    {'symbol': 'GOLD', 'name': 'Золото', 'asset_type': 'COMMODITY', 'description': 'Драгоценный металл.'},
]

print("Создание активов...")
for asset_data in assets_data:
    asset, created = Asset.objects.get_or_create(
        symbol=asset_data['symbol'],
        defaults={
            'name': asset_data['name'],
            'asset_type': asset_data['asset_type'],
            'description': asset_data['description']
        }
    )
    if created:
        print(f"  Создан: {asset.symbol}")
        
        # Генерация исторических данных о ценах
        historical = MarketDataService.fetch_historical_data(asset, 30)
        for data in historical:
            from markets.models import PriceData
            PriceData.objects.create(
                asset=asset,
                timestamp=data['date'],
                open_price=data['open'],
                high_price=data['high'],
                low_price=data['low'],
                close_price=data['close'],
                volume=data['volume']
            )

# Создание списков наблюдения
print("\nСоздание списков наблюдения...")
tech_watchlist, _ = Watchlist.objects.get_or_create(name='Технологические акции')
crypto_watchlist, _ = Watchlist.objects.get_or_create(name='Криптовалюты')

stocks = Asset.objects.filter(asset_type='STOCK')
cryptos = Asset.objects.filter(asset_type='CRYPTO')

tech_watchlist.assets.set(stocks)
crypto_watchlist.assets.set(cryptos)

print(f"  Создан: {tech_watchlist.name} ({tech_watchlist.assets.count()} активов)")
print(f"  Создан: {crypto_watchlist.name} ({crypto_watchlist.assets.count()} активов)")

# Создание новостей
print("\nСоздание новостей...")
news_items = NewsService.get_latest_news(5)
for item in news_items:
    news, created = MarketNews.objects.get_or_create(
        title=item['title'],
        defaults={
            'content': item['content'],
            'source': item['source'],
            'published_at': item['published_at']
        }
    )
    if created:
        print(f"  Создана: {news.title[:50]}...")

print("\n✅ Инициализация демо-данных завершена!")
print(f"\nВсего активов: {Asset.objects.count()}")
print(f"Всего списков наблюдения: {Watchlist.objects.count()}")
print(f"Всего новостей: {MarketNews.objects.count()}")
