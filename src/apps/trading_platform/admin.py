from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import APIKey, DealSettings, IndicatorSetting, TradingAccount, Stock


class DisableActionsIfNoAPIKeyMixin:
    def has_add_permission(self, request):
        if not APIKey.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        if not APIKey.objects.exists():
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if not APIKey.objects.exists():
            return False
        return super().has_delete_permission(request, obj)


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('api_key', 'api_secret',)
    actions = None

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('api_key',)
        return ()

    def has_add_permission(self, request):
        if APIKey.objects.exists():
            return False
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not obj.api_key:
            raise ValidationError("API Key must be set.")
        obj.save()


@admin.register(TradingAccount)
class TradingAccountAdmin(DisableActionsIfNoAPIKeyMixin, admin.ModelAdmin):
    list_display = ('name',)

    def changelist_view(self, request, extra_context=None):
        if not APIKey.objects.exists():
            self.message_user(request, "Need set API Key at first", level='error')
        return super().changelist_view(request, extra_context)


@admin.register(IndicatorSetting)
class IndicatorSettingAdmin(DisableActionsIfNoAPIKeyMixin, admin.ModelAdmin):
    list_display = ('indicator', 'numeric_value', 'recognition_method',)

    def changelist_view(self, request, extra_context=None):
        if not APIKey.objects.exists():
            self.message_user(request, "Need set API Key at first", level='error')
        return super().changelist_view(request, extra_context)


@admin.register(DealSettings)
class DealSettingsAdmin(DisableActionsIfNoAPIKeyMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('trading_account',),
        }),
        ('Indicator Settings Long', {
            'fields': ('indicator_settings_long',),
            'classes': ('collapse', 'wide', 'extrapretty',),
        }),
        ('Indicator Settings Short', {
            'fields': ('indicator_settings_short',),
            'classes': ('collapse', 'wide', 'extrapretty',),
        }),
        ('Take Profit Percentages Long', {
            'fields': (
                ('take_profit_percentage_long_time_1', 'take_profit_percentage_long_1',),
                ('take_profit_percentage_long_time_2', 'take_profit_percentage_long_2',),
                ('take_profit_percentage_long_time_3', 'take_profit_percentage_long_3',),
                ('take_profit_percentage_long_time_4', 'take_profit_percentage_long_4',),
                ('take_profit_percentage_long_time_5', 'take_profit_percentage_long_5',),
            ),
            'classes': ('collapse', 'wide', 'extrapretty',),
        }),
        ('Take Profit Percentages Short', {
            'fields': (
                ('take_profit_percentage_short_time_1', 'take_profit_percentage_short_1',),
                ('take_profit_percentage_short_time_2', 'take_profit_percentage_short_2',),
                ('take_profit_percentage_short_time_3', 'take_profit_percentage_short_3',),
                ('take_profit_percentage_short_time_4', 'take_profit_percentage_short_4',),
                ('take_profit_percentage_short_time_5', 'take_profit_percentage_short_5',),
            ),
            'classes': ('collapse', 'wide', 'extrapretty',),
        }),
        ('Long Strategy Settings', {
            'fields': (
                'enable_long_strategy',
                'stop_loss_percentage_long',
                'top_stocks_long',
            ),
            'classes': ('wide', 'extrapretty',),
        }),
        ('Short Strategy Settings', {
            'fields': (
                'enable_short_strategy',
                'stop_loss_percentage_short',
                'top_stocks_short',
            ),
            'classes': ('wide', 'extrapretty',),
        }),
        (None, {
            'fields': (
                'start_time_long',
                'start_time_short',
                'capital_allocation',
                'use_full_capital',
                'status',
            ),
        }),
    )
    list_display = (
        'trading_account',
        'enable_long_strategy',
        'enable_short_strategy',
        'start_time_long',
        'start_time_short',
        'capital_allocation',
        'use_full_capital',
        'status',
    )
    list_filter = ('status',)
    filter_horizontal = ('indicator_settings_long', 'indicator_settings_short',)

    def changelist_view(self, request, extra_context=None):
        if not APIKey.objects.exists():
            self.message_user(request, "Need set API Key at first", level='error')
        return super().changelist_view(request, extra_context)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ['indicator_settings_long', 'indicator_settings_short', ]:
            kwargs['queryset'] = IndicatorSetting.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'active',)
    search_fields = ('name',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('name',)
        return ()

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
