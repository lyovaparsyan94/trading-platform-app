import enum


class IndicatorEnum(enum.Enum):
    HIGH_DECREASING: str = 'High[-3:-1] Decreasing'
    CLOSE_GREATER_THAN_HIGH: str = 'Close Greater than High[-1]'
    CLOSE_GREATER_THAN_X: str = 'Close Greater than X'
    VOLUME_GREATER_THAN_X: str = 'Volume Greater than X'
    MA_GREATER_THAN_WMA: str = 'MA(9) Greater than WMA(5)'
    RSI_CROSSED_ABOVE_X: str = 'RSI(14) crossed above X'
    RSI_GREATER_THAN_X: str = 'RSI(14) Greater than X'
    CLOSE_CROSSED_ABOVE_MA: str = 'Close crossed above MA(9)'
    CCI_GREATER_THAN_X: str = 'CCI(14) Greater than X'
    AROONUP_GREATER_THAN_X: str = 'AROONUP(25) Greater than X'
    AROONDOWN_LESS_THAN_X: str = 'AROONDOWN(25) Less than X'
    ADX_GREATER_THAN_X: str = 'ADX(8) Greater than X'
    MA3_GREATER_THAN_MA9: str = 'MA(3) Greater than MA(9)'
    ADX13_GREATER_THAN_X: str = 'ADX(13) Greater than X'
    DI_PLUS_ABOVE_X: str = '+DI(13) is above X'
    DI_MINUS_BELOW_X: str = '-DI below X'
