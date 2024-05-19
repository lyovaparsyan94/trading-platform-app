from enum import Enum
from src.apps.trading_platform.models import Indicator, IndicatorSetting


class IndicatorEnum(Enum):
    indicators = Indicator.objects.all().values_list('name', flat=True)
    HIGH_DECREASING = indicators[0]
    CLOSE_GREATER_THAN_HIGH = indicators[1]
    CLOSE_GREATER_THAN_X = indicators[2]
    VOLUME_GREATER_THAN_X = indicators[3]
    MA_GREATER_THAN_WMA = indicators[4]
    RSI_CROSSED_ABOVE_X = indicators[5]
    RSI_GREATER_THAN_X = indicators[6]
    CLOSE_CROSSED_ABOVE_MA = indicators[7]
    CCI_GREATER_THAN_X = indicators[8]
    AROONUP_GREATER_THAN_X = indicators[9]
    AROONDOWN_LESS_THAN_X = indicators[10]
    ADX_GREATER_THAN_X = indicators[11]
    MA3_GREATER_THAN_MA9 = indicators[12]
    ADX13_GREATER_THAN_X = indicators[13]
    DI_PLUS_ABOVE_X = indicators[14]
    DI_MINUS_BELOW_X = indicators[15]
