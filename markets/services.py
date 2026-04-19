import requests
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Asset, PriceData


class MarketDataService:
    """Сервис для получения рыночных данных из внешних API"""
    
    # Демо-данные для демонстрации (в продакшене используйте реальные API: Alpha Vantage, Yahoo Finance и т.д.)
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
        """Получить текущую цену актива (демо-реализация)"""
        import random
        
        if symbol not in cls.MOCK_PRICES:
            return None
        
        mock_data = cls.MOCK_PRICES[symbol]
        base_price = mock_data['base']
        volatility = mock_data['volatility']
        
        # Генерация реалистичного движения цены
        change_percent = random.uniform(-volatility, volatility)
        current_price = base_price * (1 + change_percent)
        
        # Обновление базовой цены для следующего вызова (симуляция движения рынка)
        cls.MOCK_PRICES[symbol]['base'] = current_price
        
        return {
            'symbol': symbol,
            'price': round(current_price, 2),
            'change_percent': round(change_percent * 100, 2),
            'timestamp': timezone.now(),
        }
    
    @classmethod
    def fetch_historical_data(cls, asset, days=30):
        """Получить исторические данные о ценах актива"""
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
        """Обновить данные о ценах актива"""
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
    """Сервис для получения новостей рынка"""
    
    MOCK_NEWS = [
        {
            'title': 'Технологические акции растут на фоне сильных отчетов',
            'content': 'Крупные технологические компании отчитались о прибыли выше ожиданий, что привело к росту акций сектора.',
            'source': 'Market Watch',
        },
        {
            'title': 'ФРС сигнализирует о возможных изменениях ставок',
            'content': 'Федеральная резервная система намекнула на возможную корректировку процентных ставок в ответ на экономические показатели.',
            'source': 'Financial Times',
        },
        {
            'title': 'Рынок криптовалют показывает волатильность на фоне регуляторных новостей',
            'content': 'Биткоин и другие криптовалюты испытали значительные колебания цен после заявлений регуляторов.',
            'source': 'Crypto Daily',
        },
        {
            'title': 'Цены на нефть колеблются из-за опасений по поводу поставок',
            'content': 'Цены на сырую нефть изменились, поскольку трейдеры оценивали глобальную динамику поставок и геополитическую напряженность.',
            'source': 'Energy Report',
        },
        {
            'title': 'Европейские рынки закрылись ростом на экономических данных',
            'content': 'Европейские фондовые индексы завершили торговую сессию ростом после публикации положительных экономических данных.',
            'source': 'EU Markets',
        },
    ]
    
    @classmethod
    def get_latest_news(cls, limit=10):
        """Получить последние новости рынка"""
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
