from django.db import models


class APIKey(models.Model):
    api_key = models.CharField(max_length=256, verbose_name="API Key", blank=False)
    api_secret = models.CharField(max_length=256, verbose_name="API Secret", blank=False)

    def __str__(self):
        return self.api_key

    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Key"


class TradingAccount(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True, verbose_name="Name")

    def __str__(self):
        return self.name or "Unnamed Account"

    class Meta:
        verbose_name = "Trading Account"
        verbose_name_plural = "Trading Accounts"


class DealSettings(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    trading_account = models.ForeignKey(TradingAccount, on_delete=models.CASCADE, verbose_name="Trading Account")
    status = models.CharField(max_length=16, choices=StatusChoices.choices, default=StatusChoices.INACTIVE,
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

    def __str__(self):
        return f"DealSettings for {self.trading_account} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Deal Settings"
        verbose_name_plural = "Deal Settings"


class StockMonitorConfiguration(models.Model):
    email = models.EmailField(verbose_name="Email")
    password = models.CharField(max_length=256, verbose_name="Password")
    long_strategy_payload = models.JSONField(default=dict, verbose_name="Long Strategy Payload")
    short_strategy_payload = models.JSONField(default=dict, verbose_name="Short Strategy Payload")
    stockmonitor_cookies = models.JSONField(default=dict, verbose_name="Stock Monitor Cookies")

    def __str__(self):
        return "Stock Monitor Configuration"

    class Meta:
        verbose_name = "Stock Monitor Configuration"
        verbose_name_plural = "Stock Monitor Configurations"
