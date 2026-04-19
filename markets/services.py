import requests
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Asset, PriceData


class MarketDataService:
    """Service for fetching market data from external APIs"""
    
    # Mock data for demonstration (in production, use real API like Alpha Vantage, Yahoo Finance, etc.)
    MOCK_PRICES = {
        'AAPL': {'base': 175.0, 'volatility': 0.02},
        'GOOGL': {'base': 140.0, 'volatility': 0.025},
        'MSFT': {'base': 380.0, 'volatility': 0.018},
        'TSLA': {'base': 250.0, 'volatility': 0.035},
        'BTC': {'base': 45000.0, 'volatility': 0.05},
        'ETH': {'base': 2800.0, 'volatility': 0.045},
        'EURUSD': {'base': 1.08, 'volatility': 0.005},
        'GOLD': {'base': 2000.0, 'volatility': 0.012},
    }
    
    @classmethod
    def get_asset_price(cls, symbol):
        """Get current price for an asset (mock implementation)"""
        import random
        
        if symbol not in cls.MOCK_PRICES:
            return None
        
        mock_data = cls.MOCK_PRICES[symbol]
        base_price = mock_data['base']
        volatility = mock_data['volatility']
        
        # Generate realistic price movement
        change_percent = random.uniform(-volatility, volatility)
        current_price = base_price * (1 + change_percent)
        
        # Update base for next call (simulate market movement)
        cls.MOCK_PRICES[symbol]['base'] = current_price
        
        return {
            'symbol': symbol,
            'price': round(current_price, 2),
            'change_percent': round(change_percent * 100, 2),
            'timestamp': timezone.now(),
        }
    
    @classmethod
    def fetch_historical_data(cls, asset, days=30):
        """Fetch historical price data for an asset"""
        import random
        
        if asset.symbol not in cls.MOCK_PRICES:
            return []
        
        mock_data = cls.MOCK_PRICES[asset.symbol]
        base_price = mock_data['base']
        volatility = mock_data['volatility']
        
        historical = []
        current_price = base_price
        
        for i in range(days):
            date = timezone.now() - timedelta(days=days - i)
            change_percent = random.uniform(-volatility, volatility)
            open_price = current_price
            close_price = current_price * (1 + change_percent)
            high_price = max(open_price, close_price) * (1 + random.uniform(0, volatility/2))
            low_price = min(open_price, close_price) * (1 - random.uniform(0, volatility/2))
            volume = random.randint(1000000, 100000000)
            
            historical.append({
                'date': date,
                'open': round(open_price, 2),
                'high': round(high_price, 2),
                'low': round(low_price, 2),
                'close': round(close_price, 2),
                'volume': volume,
            })
            
            current_price = close_price
        
        return historical
    
    @classmethod
    def update_asset_prices(cls, asset):
        """Update price data for an asset"""
        price_data = cls.get_asset_price(asset.symbol)
        
        if price_data:
            PriceData.objects.create(
                asset=asset,
                timestamp=price_data['timestamp'],
                open_price=price_data['price'],
                high_price=price_data['price'] * 1.001,
                low_price=price_data['price'] * 0.999,
                close_price=price_data['price'],
                volume=1000000,
            )
            return True
        return False


class NewsService:
    """Service for fetching market news"""
    
    MOCK_NEWS = [
        {
            'title': 'Tech Stocks Rally on Strong Earnings Reports',
            'content': 'Major technology companies reported better-than-expected quarterly earnings, driving stock prices higher across the sector.',
            'source': 'Market Watch',
        },
        {
            'title': 'Federal Reserve Signals Potential Rate Changes',
            'content': 'The Federal Reserve indicated possible adjustments to interest rates in response to economic indicators.',
            'source': 'Financial Times',
        },
        {
            'title': 'Cryptocurrency Market Shows Volatility Amid Regulatory News',
            'content': 'Bitcoin and other cryptocurrencies experienced significant price movements following regulatory announcements.',
            'source': 'Crypto Daily',
        },
        {
            'title': 'Oil Prices Fluctuate on Global Supply Concerns',
            'content': 'Crude oil prices varied as traders assessed global supply dynamics and geopolitical tensions.',
            'source': 'Energy Report',
        },
        {
            'title': 'European Markets Close Higher on Economic Data',
            'content': 'European stock indices ended the trading session with gains after positive economic data releases.',
            'source': 'EU Markets',
        },
    ]
    
    @classmethod
    def get_latest_news(cls, limit=10):
        """Get latest market news"""
        import random
        from datetime import timedelta
        
        news_items = []
        for i, mock in enumerate(cls.MOCK_NEWS[:limit]):
            news_items.append({
                'title': mock['title'],
                'content': mock['content'],
                'source': mock['source'],
                'published_at': timezone.now() - timedelta(hours=i*2),
            })
        
        return news_items
