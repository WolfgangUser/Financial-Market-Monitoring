import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_monitor.settings')
django.setup()

from markets.models import Asset, Watchlist, MarketNews
from markets.services import MarketDataService, NewsService
from django.utils import timezone
from datetime import timedelta

# Create sample assets
assets_data = [
    {'symbol': 'AAPL', 'name': 'Apple Inc.', 'asset_type': 'STOCK', 'description': 'Technology company that designs and manufactures consumer electronics.'},
    {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'asset_type': 'STOCK', 'description': 'Multinational technology conglomerate holding company.'},
    {'symbol': 'MSFT', 'name': 'Microsoft Corporation', 'asset_type': 'STOCK', 'description': 'Technology corporation producing computer software, consumer electronics.'},
    {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'asset_type': 'STOCK', 'description': 'Electric vehicle and clean energy company.'},
    {'symbol': 'BTC', 'name': 'Bitcoin', 'asset_type': 'CRYPTO', 'description': 'Decentralized digital cryptocurrency.'},
    {'symbol': 'ETH', 'name': 'Ethereum', 'asset_type': 'CRYPTO', 'description': 'Open-source blockchain platform with smart contract functionality.'},
    {'symbol': 'EURUSD', 'name': 'Euro / US Dollar', 'asset_type': 'FOREX', 'description': 'Currency pair representing Euro against US Dollar.'},
    {'symbol': 'GOLD', 'name': 'Gold', 'asset_type': 'COMMODITY', 'description': 'Precious metal commodity.'},
]

print("Creating assets...")
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
        print(f"  Created: {asset.symbol}")
        
        # Generate historical price data
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

# Create sample watchlists
print("\nCreating watchlists...")
tech_watchlist, _ = Watchlist.objects.get_or_create(name='Tech Stocks')
crypto_watchlist, _ = Watchlist.objects.get_or_create(name='Cryptocurrencies')

stocks = Asset.objects.filter(asset_type='STOCK')
cryptos = Asset.objects.filter(asset_type='CRYPTO')

tech_watchlist.assets.set(stocks)
crypto_watchlist.assets.set(cryptos)

print(f"  Created: {tech_watchlist.name} ({tech_watchlist.assets.count()} assets)")
print(f"  Created: {crypto_watchlist.name} ({crypto_watchlist.assets.count()} assets)")

# Create sample news
print("\nCreating news...")
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
        print(f"  Created: {news.title[:50]}...")

print("\n✅ Sample data initialization complete!")
print(f"\nTotal assets: {Asset.objects.count()}")
print(f"Total watchlists: {Watchlist.objects.count()}")
print(f"Total news items: {MarketNews.objects.count()}")
