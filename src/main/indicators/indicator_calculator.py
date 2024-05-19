from src.main.indicators.indicators import IndicatorCalculator
from src.apps.trading_platform.models import Indicator, IndicatorSetting
from src.main.indicators.indicator_enum import IndicatorEnum


def calculate_indicator(indicator_name, data):
    try:
        indicator = Indicator.objects.get(name=indicator_name)
    except Indicator.DoesNotExist as e:
        raise ValueError(f"Indicator '{indicator_name}' not found: {e}")

    try:
        setting = IndicatorSetting.objects.get(indicator=indicator)
    except IndicatorSetting.DoesNotExist as e:
        raise ValueError(f"Setting for indicator '{indicator_name}' not found: {e}")

    # Create an instance of the calculator
    calculator = IndicatorCalculator(data)

    # Map indicator name to enum
    indicator_enum = IndicatorEnum(indicator_name)

    # Call the appropriate method based on the indicator enum
    if indicator_enum == IndicatorEnum.HIGH_DECREASING:
        result = calculator.high_decreasing()
    if indicator_enum == IndicatorEnum.CLOSE_GREATER_THAN_HIGH:
        result = calculator.close_greater_than_high()
    if indicator_enum == IndicatorEnum.CLOSE_GREATER_THAN_X:
        result = calculator.close_greater_than_x(setting.numeric_value)
    if indicator_enum == IndicatorEnum.VOLUME_GREATER_THAN_X:
        result = calculator.volume_greater_than_x(setting.numeric_value)
    if indicator_enum == IndicatorEnum.MA_GREATER_THAN_WMA:
        result = calculator.ma_greater_than_wma()
    if indicator_enum == IndicatorEnum.RSI_CROSSED_ABOVE_X:
        result = calculator.rsi_crossed_above(x=setting.numeric_value)
    if indicator_enum == IndicatorEnum.RSI_GREATER_THAN_X:
        result = calculator.rsi_greater_than_x(x=setting.numeric_value)

    return result
