from typing import Any
from django.db.models import Model
from django.contrib import admin
from .models import TradingAccount, IndicatorSetting, DealSettings
from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    admin.site.site_header = 'Trading Platform'


admin_site = CustomAdminSite()


@admin.register(TradingAccount)
class TradingAccountAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'api_key',
                    )


@admin.register(IndicatorSetting)
class IndicatorSettingAdmin(admin.ModelAdmin):
    list_display = ('indicator',
                    'numeric_value',
                    'recognition_method',
                    )


@admin.register(DealSettings)
class DealSettingsAdmin(admin.ModelAdmin):
    list_display = ('trading_account',
                    'strategy_choice',
                    'status',
                    )
    list_filter = ('status', 'strategy_choice',)
    filter_horizontal = ('indicator_settings',)

    def formfield_for_foreignkey(self, db_field: Model, request: Any, **kwargs: Any) -> Any:
        """
        Customizes the form field for a ForeignKey field.

        Args:
            db_field (Model): The ForeignKey field.
            request (Any): The request object.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            Any: The modified form field.
        """
        if db_field.name == 'indicator_settings':
            kwargs['queryset'] = IndicatorSetting.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
