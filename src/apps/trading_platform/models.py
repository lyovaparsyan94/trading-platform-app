from django.core.exceptions import ValidationError
from django.db import models


class APIKey(models.Model):
    api_key = models.CharField(max_length=255, verbose_name="API Key")
    api_secret = models.CharField(max_length=255, verbose_name="API Secret")

    def __str__(self):
        return self.api_key

    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Key"


class TradingAccount(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Name")

    def __str__(self):
        return self.name or "Unnamed Account"

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

    trading_account = models.ForeignKey(TradingAccount, on_delete=models.CASCADE, verbose_name="Trading Account")
    indicator_settings_long = models.ManyToManyField(IndicatorSetting, related_name="indicator_settings_long",
                                                     verbose_name="Indicator Settings Long")
    indicator_settings_short = models.ManyToManyField(IndicatorSetting, related_name="indicator_settings_short",
                                                      verbose_name="Indicator Settings Short")
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.INACTIVE,
                              verbose_name="Status")

    enable_long_strategy = models.BooleanField(default=False, verbose_name="Enable Long Strategy")
    enable_short_strategy = models.BooleanField(default=False, verbose_name="Enable Short Strategy")

    start_time_long = models.IntegerField(verbose_name="Start Time Long (minutes after market open)", null=True,
                                          blank=True)
    start_time_short = models.IntegerField(verbose_name="Start Time Short (minutes after market open)", null=True,
                                           blank=True)

    top_stocks_long = models.IntegerField(verbose_name="Top Stocks for Long Strategy", null=True, blank=True)
    top_stocks_short = models.IntegerField(verbose_name="Top Stocks for Short Strategy", null=True, blank=True)

    take_profit_percentage_long_1 = models.FloatField(verbose_name="Percentage Long (1st sequence)", null=True,
                                                      blank=True)
    take_profit_percentage_long_time_1 = models.IntegerField(verbose_name="Time in minutes (1st sequence)", null=True,
                                                             blank=True)
    take_profit_percentage_long_2 = models.FloatField(verbose_name="Percentage Long (2nd sequence)", null=True,
                                                      blank=True)
    take_profit_percentage_long_time_2 = models.IntegerField(verbose_name="Time in minutes (2nd sequence)", null=True,
                                                             blank=True)
    take_profit_percentage_long_3 = models.FloatField(verbose_name="Percentage Long (3rd sequence)", null=True,
                                                      blank=True)
    take_profit_percentage_long_time_3 = models.IntegerField(verbose_name="Time in minutes (3rd sequence)", null=True,
                                                             blank=True)
    take_profit_percentage_long_4 = models.FloatField(verbose_name="Percentage Long (4th sequence)", null=True,
                                                      blank=True)
    take_profit_percentage_long_time_4 = models.IntegerField(verbose_name="Time in minutes (4th sequence)", null=True,
                                                             blank=True)
    take_profit_percentage_long_5 = models.FloatField(verbose_name="Percentage Long (final sequence)", null=True,
                                                      blank=True)
    take_profit_percentage_long_time_5 = models.IntegerField(verbose_name="Time in minutes (final sequence)", null=True,
                                                             blank=True)

    take_profit_percentage_short_1 = models.FloatField(verbose_name="Percentage Short (1st sequence)", null=True,
                                                       blank=True)
    take_profit_percentage_short_time_1 = models.IntegerField(verbose_name="Time in minutes (1st sequence)", null=True,
                                                              blank=True)
    take_profit_percentage_short_2 = models.FloatField(verbose_name="Percentage Short (2nd sequence)", null=True,
                                                       blank=True)
    take_profit_percentage_short_time_2 = models.IntegerField(verbose_name="Time in minutes (2nd sequence)", null=True,
                                                              blank=True)
    take_profit_percentage_short_3 = models.FloatField(verbose_name="Percentage Short (3rd sequence)", null=True,
                                                       blank=True)
    take_profit_percentage_short_time_3 = models.IntegerField(verbose_name="Time in minutes (3rd sequence)", null=True,
                                                              blank=True)
    take_profit_percentage_short_4 = models.FloatField(verbose_name="Percentage Short (4th sequence)", null=True,
                                                       blank=True)
    take_profit_percentage_short_time_4 = models.IntegerField(verbose_name="Time in minutes (4th sequence)", null=True,
                                                              blank=True)
    take_profit_percentage_short_5 = models.FloatField(verbose_name="Percentage Short (final sequence)", null=True,
                                                       blank=True)
    take_profit_percentage_short_time_5 = models.IntegerField(verbose_name="Time in minutes (final sequence)",
                                                              null=True, blank=True)
    stop_loss_percentage_long = models.FloatField(verbose_name="Stop Loss Percentage Long", null=True, blank=True)
    stop_loss_percentage_short = models.FloatField(verbose_name="Stop Loss Percentage Short", null=True, blank=True)

    capital_allocation = models.FloatField(verbose_name="Capital Allocation", null=True, blank=True)
    use_full_capital = models.BooleanField(default=False, verbose_name="Use Full Capital")

    def clean(self):
        if not APIKey.objects.filter(api_key__isnull=False).exists():
            raise ValidationError("API Key must be set before any operations can be performed.")
        if self.use_full_capital and self.capital_allocation is not None:
            raise ValidationError("If 'Use Full Capital' is selected, 'Capital Allocation' should be empty.")
        if not self.use_full_capital and self.capital_allocation is None:
            raise ValidationError("If 'Use Full Capital' is not selected, 'Capital Allocation' should be provided.")
        if not self.enable_long_strategy and not self.enable_short_strategy:
            raise ValidationError("At least one strategy (long or short) must be enabled.")

    def __str__(self):
        return f"DealSettings for {self.trading_account} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Deal Settings"
        verbose_name_plural = "Deal Settings"
