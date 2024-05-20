from django.db import models


class TradingAccount(models.Model):
    api_key = models.CharField(max_length=255, verbose_name="API Key")
    api_secret = models.CharField(max_length=255, verbose_name="API Secret")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Name")

    def __str__(self):
        return self.name or self.api_key

    class Meta:
        verbose_name = "Trading Account"
        verbose_name_plural = "Trading Accounts"


class Indicator(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Indicator"
        verbose_name_plural = "Indicators"


class IndicatorSetting(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name="settings",
                                  verbose_name="Indicator")
    numeric_value = models.FloatField(verbose_name="Numeric Value")
    recognition_method = models.CharField(max_length=50, blank=True, null=True, verbose_name="Recognition Method")

    def __str__(self):
        return f"{self.indicator.name} ({self.numeric_value})"

    class Meta:
        verbose_name = "Indicator Setting"
        verbose_name_plural = "Indicator Settings"


class DealSettings(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    class StrategyChoices(models.TextChoices):
        LONG = 'long', 'Long'
        SHORT = 'short', 'Short'

    trading_account = models.ForeignKey(TradingAccount, on_delete=models.CASCADE, verbose_name="Trading Account")
    indicator_settings = models.ManyToManyField(IndicatorSetting, verbose_name="Indicator Settings")
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.INACTIVE,
                              verbose_name="Status")
    strategy_choice = models.CharField(max_length=10, choices=StrategyChoices.choices, verbose_name="Strategy Choice")

    def __str__(self):
        return f"DealSettings for {self.trading_account} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Deal Settings"
        verbose_name_plural = "Deal Settings"
