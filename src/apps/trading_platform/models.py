from django.db import models


class TradingAccount(models.Model):
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name if self.name else self.api_key


class Indicator(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class IndicatorSetting(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    numeric_value = models.FloatField()
    recognition_method = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.indicator.name} ({self.numeric_value})"


class DealSettings(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    trading_account = models.ForeignKey(TradingAccount, on_delete=models.CASCADE)
    indicator_settings = models.ManyToManyField(IndicatorSetting)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')
    strategy_choice = models.CharField(max_length=10, choices=[('long', 'Long'), ('short', 'Short')])

    def __str__(self):
        return f"DealSettings for {self.trading_account} ({self.get_status_display()})"
