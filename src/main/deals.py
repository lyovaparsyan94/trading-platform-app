import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.core.settings")
django.setup()

from src.main.indicators.indicator_enum import IndicatorEnum
from src.main.indicators.indicator_calculator import calculate_indicator
from src.apps.trading_platform.models import Indicator, IndicatorSetting

data = {
    'High': [100, 110, 105, 98],
    'Close': [98, 105, 102, 100],
    'Volume': [10000, 12000, 11000, 10500]
}
# indicators = Indicator.objects.all()
indicators = Indicator.objects.all().values_list('name', flat=True)
for i in indicators:
    print(f"{i} ")
