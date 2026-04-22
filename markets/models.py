from django.db import models
from django.utils import timezone


class Asset(models.Model):
    """Модель финансового актива (акция, валюта, криптовалюта и т.д.)"""
    ASSET_TYPES = [
        ('STOCK', 'Акция'),
        ('FOREX', 'Форекс'),
        ('CRYPTO', 'Криптовалюта'),
        ('COMMODITY', 'Товар'),
        ('INDEX', 'Индекс'),
    ]

    symbol = models.CharField(max_length=20, unique=True, verbose_name='Символ')
    name = models.CharField(max_length=200, verbose_name='Название')
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES, verbose_name='Тип актива')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        ordering = ['symbol']
        verbose_name = 'Актив'
        verbose_name_plural = 'Активы'

    def __str__(self):
        return f"{self.symbol} - {self.name}"


class PriceData(models.Model):
    """Модель данных о ценах активов"""
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='prices', verbose_name='Актив')
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='Время')
    open_price = models.DecimalField(max_digits=15, decimal_places=6, verbose_name='Цена открытия')
    high_price = models.DecimalField(max_digits=15, decimal_places=6, verbose_name='Максимальная цена')
    low_price = models.DecimalField(max_digits=15, decimal_places=6, verbose_name='Минимальная цена')
    close_price = models.DecimalField(max_digits=15, decimal_places=6, verbose_name='Цена закрытия')
    volume = models.BigIntegerField(default=0, verbose_name='Объем')

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['asset', '-timestamp']),
        ]
        verbose_name = 'Данные о цене'
        verbose_name_plural = 'Данные о ценах'

    def __str__(self):
        return f"{self.asset.symbol} @ {self.close_price} ({self.timestamp})"


class Watchlist(models.Model):
    """Список наблюдения для отслеживания избранных активов"""
    name = models.CharField(max_length=100, verbose_name='Название')
    assets = models.ManyToManyField(Asset, related_name='watchlists', verbose_name='Активы')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['name']
        verbose_name = 'Список наблюдения'
        verbose_name_plural = 'Списки наблюдения'

    def __str__(self):
        return self.name


class MarketNews(models.Model):
    """Новости и объявления рынка"""
    title = models.CharField(max_length=300, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    source = models.CharField(max_length=200, verbose_name='Источник')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    related_assets = models.ManyToManyField(Asset, blank=True, related_name='news', verbose_name='Связанные активы')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Новость рынка'
        verbose_name_plural = 'Новости рынка'

    def __str__(self):
        return self.title
