from django.db import models
from django.utils import timezone


class Asset(models.Model):
    """Model representing a financial asset (stock, currency, crypto, etc.)"""
    ASSET_TYPES = [
        ('STOCK', 'Stock'),
        ('FOREX', 'Forex'),
        ('CRYPTO', 'Cryptocurrency'),
        ('COMMODITY', 'Commodity'),
        ('INDEX', 'Index'),
    ]

    symbol = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['symbol']

    def __str__(self):
        return f"{self.symbol} - {self.name}"


class PriceData(models.Model):
    """Model storing price data for assets"""
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='prices')
    timestamp = models.DateTimeField(default=timezone.now)
    open_price = models.DecimalField(max_digits=15, decimal_places=6)
    high_price = models.DecimalField(max_digits=15, decimal_places=6)
    low_price = models.DecimalField(max_digits=15, decimal_places=6)
    close_price = models.DecimalField(max_digits=15, decimal_places=6)
    volume = models.BigIntegerField(default=0)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['asset', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.asset.symbol} @ {self.close_price} ({self.timestamp})"


class Watchlist(models.Model):
    """User watchlist for tracking favorite assets"""
    name = models.CharField(max_length=100)
    assets = models.ManyToManyField(Asset, related_name='watchlists')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class MarketNews(models.Model):
    """Market news and announcements"""
    title = models.CharField(max_length=300)
    content = models.TextField()
    source = models.CharField(max_length=200)
    published_at = models.DateTimeField()
    related_assets = models.ManyToManyField(Asset, blank=True, related_name='news')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
