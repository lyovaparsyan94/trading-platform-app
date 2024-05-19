from enum import Enum
from typing import Callable, Optional
from src.apps.trading_platform.indicators.indicators import Indicators
from src.apps.trading_platform.models import Indicator


class IndicatorEnum(Enum):
    indicators = Indicator.objects.all().values_list('name', flat=True)
    HIGH_DECREASING: str = indicators[0]
    CLOSE_GREATER_THAN_HIGH: str = indicators[1]
    CLOSE_GREATER_THAN_X: str = indicators[2]
    VOLUME_GREATER_THAN_X: str = indicators[3]
    MA_GREATER_THAN_WMA: str = indicators[4]
    RSI_CROSSED_ABOVE_X: str = indicators[5]
    RSI_GREATER_THAN_X: str = indicators[6]
    CLOSE_CROSSED_ABOVE_MA: str = indicators[7]
    CCI_GREATER_THAN_X: str = indicators[8]
    AROONUP_GREATER_THAN_X: str = indicators[9]
    AROONDOWN_LESS_THAN_X: str = indicators[10]
    ADX_GREATER_THAN_X: str = indicators[11]
    MA3_GREATER_THAN_MA9: str = indicators[12]
    ADX13_GREATER_THAN_X: str = indicators[13]
    DI_PLUS_ABOVE_X: str = indicators[14]
    DI_MINUS_BELOW_X: str = indicators[15]

    def get_required_indicator_function(self, indicator_name: str) -> Optional[Callable]:
        """
        Get the required indicator function based on the given indicator name.

        Args:
            indicator_name (str): The name of the indicator.

        Returns:
            Optional[Callable]: The corresponding indicator function.
        """
        function_map = {
            'High[-3:-1] Decreasing': Indicators.high_decreasing,
            'Close Greater than High[-1]': Indicators.close_greater_than_high,
            'Close Greater than X': Indicators.close_greater_than_x,
            'Volume Greater than X': Indicators.volume_greater_than_x,
            'MA(9) Greater than WMA(5)': Indicators.ma_greater_than_wma,
            'RSI(14) crossed above X': Indicators.rsi_crossed_above,
            'RSI(14) Greater than X': Indicators.rsi_greater_than_x,
            'Close crossed above MA(9)': Indicators.close_crossed_above_ma,
            'CCI(14) Greater than X': Indicators.cci_greater_than_x,
            'AROONUP(25) Greater than X': Indicators.aroon_up_greater_than_x,
            'AROONDOWN(25) Less than X': Indicators.aroon_down_less_than_x,
            'ADX(8) Greater than X': Indicators.adx_greater_than_x,
            'MA(3) Greater than MA(9)': Indicators.ma3_greater_than_ma9,
            'ADX(13) Greater than X': Indicators.adx_greater_than_x,
            '+DI(13) is above X': Indicators.di_plus_above_x,
            '-DI below X': Indicators.di_minus_below_x,
        }

        return function_map.get(indicator_name)
