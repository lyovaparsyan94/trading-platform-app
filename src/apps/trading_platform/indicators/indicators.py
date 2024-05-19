import numpy as np
from typing import Dict, Any


class Indicators:
    """
    A class containing methods to calculate various technical indicators.
    """

    def high_decreasing(self, data: Dict[str, Any], period: int = 3) -> bool:
        """
        Check if the highest price is decreasing over a specified period.

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            period (int): Period for the check.

        Returns:
            bool: True if the highest price is decreasing over the specified period, False otherwise.
        """
        return all(data['High'][i] < data['High'][i - 1] for i in range(-period, 0))

    def close_greater_than_high(self, data: Dict[str, Any]) -> bool:
        """
        Check if the closing price is greater than the highest price.

        Args:
            data (Dict[str, Any]): Dictionary containing market data.

        Returns:
            bool: True if the closing price is greater than the highest price, False otherwise.
        """
        return data['Close'][-1] > data['High'][-2]

    def close_greater_than_x(self, data: Dict[str, Any], x: float) -> bool:
        """
        Check if the closing price is greater than a specified value (x).

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            x (float): Value to compare the closing price against.

        Returns:
            bool: True if the closing price is greater than x, False otherwise.
        """
        return data['Close'][-1] > x

    def volume_greater_than_x(self, data: Dict[str, Any], x: float) -> bool:
        """
        Check if the volume is greater than a specified value (x).

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            x (float): Value to compare the volume against.

        Returns:
            bool: True if the volume is greater than x, False otherwise.
        """
        return data['Volume'][-1] > x

    def ma(self, data: Dict[str, Any], period: int) -> float:
        """
        Calculate the moving average (MA) of the Close price over a specified period.

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            period (int): Period for the moving average calculation.

        Returns:
            float: Moving average of the Close price.
        """
        return np.mean(data['Close'][-period:])

    def wma(self, data: Dict[str, Any], period: int) -> float:
        """
        Calculate the weighted moving average (WMA) of the Close price over a specified period.

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            period (int): Period for the weighted moving average calculation.

        Returns:
            float: Weighted moving average of the Close price.
        """
        weights = np.arange(1, period + 1)
        weighted_sum = np.dot(data['Close'][-period:], weights[::-1])
        return weighted_sum / weights.sum()

    def ma_greater_than_wma(self, data: Dict[str, Any], ma_period: int = 9, wma_period: int = 5) -> bool:
        """
        Check if the moving average (MA) is greater than the weighted moving average (WMA).

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            ma_period (int): Period for the MA calculation.
            wma_period (int): Period for the WMA calculation.

        Returns:
            bool: True if the MA is greater than the WMA, False otherwise.
        """
        return self.ma(data, ma_period) > self.wma(data, wma_period)

    def rsi(self, data: Dict[str, Any], period: int = 14) -> float:
        """
        Calculate the Relative Strength Index (RSI) over a specified period.

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            period (int): Period for the RSI calculation.

        Returns:
            float: Relative Strength Index (RSI).
        """
        deltas = np.diff(data['Close'])
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)

        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def rsi_crossed_above(self, data: Dict[str, Any], period: int = 14, x: float = 30) -> bool:
        """
        Check if the RSI has crossed above a specified value (x) over a specified period.

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            period (int): Period for the RSI calculation.
            x (float): Value to compare the RSI against.

        Returns:
            bool: True if the RSI has crossed above x, False otherwise.
        """
        prev_rsi = self.rsi(data, period - 1)
        curr_rsi = self.rsi(data, period)
        return prev_rsi < x < curr_rsi

    def rsi_greater_than_x(self, data: Dict[str, Any], period: int = 14, x: float = 70) -> bool:
        """
        Check if the RSI is greater than a specified value (x) over a specified period.

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            period (int): Period for the RSI calculation.
            x (float): Value to compare the RSI against.

        Returns:
            bool: True if the RSI is greater than x, False otherwise.
        """
        return self.rsi(data, period) > x

    def close_crossed_above_ma(self, data: Dict[str, Any], ma_period: int = 9) -> bool:
        """
        Check if the closing price has crossed above the moving average (MA).

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            ma_period (int): Period for the MA calculation.

        Returns:
            bool: True if the closing price has crossed above the MA, False otherwise.
        """
        ma_value = self.ma(data, ma_period)
        return data['Close'][-2] < ma_value < data['Close'][-1]

    def cci(self, data: Dict[str, Any], period: int = 14, constant: float = 0.015) -> float:
        """
        Calculate the Commodity Channel Index (CCI) over a specified period.

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            period (int): Period for the CCI calculation.
            constant (float): Constant value for the CCI calculation.

        Returns:
            float: Commodity Channel Index (CCI).
        """
        high = np.array(data['High'][-        period:])
        low = np.array(data['Low'][-period:])
        close = np.array(data['Close'][-period:])
        tp = (high + low + close) / 3

        ma_tp = np.mean(tp)
        mean_deviation = np.mean(np.abs(tp - ma_tp))

        if mean_deviation == 0:
            return 0

        return (tp[-1] - ma_tp) / (constant * mean_deviation)

    def cci_greater_than_x(self, data: Dict[str, Any], period: int = 14, x: float = 100) -> bool:
        """
        Check if the Commodity Channel Index (CCI) is greater than a specified value (x) over a specified period.

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            period (int): Period for the CCI calculation.
            x (float): Value to compare the CCI against.

        Returns:
            bool: True if the CCI is greater than x, False otherwise.
        """
        return self.cci(data, period) > x

    def aroon(self, data: Dict[str, Any], period: int = 25) -> tuple:
        """
        Calculate the Aroon indicators over a specified period.

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            period (int): Period for the Aroon calculation.

        Returns:
            tuple: A tuple containing Aroon Up and Aroon Down values.
        """
        high_idx = np.argmax(data['High'][-period:])
        low_idx = np.argmin(data['Low'][-period:])
        aroon_up = ((period - high_idx - 1) / period) * 100
        aroon_down = ((period - low_idx - 1) / period) * 100
        return aroon_up, aroon_down

    def aroon_up_greater_than_x(self, data: Dict[str, Any], period: int = 25, x: float = 70) -> bool:
        """
        Check if the Aroon Up indicator is greater than a specified value (x) over a specified period.

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            period (int): Period for the Aroon calculation.
            x (float): Value to compare the Aroon Up against.

        Returns:
            bool: True if the Aroon Up is greater than x, False otherwise.
        """
        aroon_up, _ = self.aroon(data, period)
        return aroon_up > x

    def aroon_down_less_than_x(self, data: Dict[str, Any], period: int = 25, x: float = 30) -> bool:
        """
        Check if the Aroon Down indicator is less than a specified value (x) over a specified period.

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            period (int): Period for the Aroon calculation.
            x (float): Value to compare the Aroon Down against.

        Returns:
            bool: True if the Aroon Down is less than x, False otherwise.
        """
        _, aroon_down = self.aroon(data, period)
        return aroon_down < x

    def ma3_greater_than_ma9(self, data: Dict[str, Any]) -> bool:
        """
        Check if the 3-day moving average (MA) is greater than the 9-day MA.

        Args:
            data (Dict[str, Any]): Dictionary containing market data.

        Returns:
            bool: True if the 3-day MA is greater than the 9-day MA, False otherwise.
        """
        return self.ma(data, 3) > self.ma(data, 9)

    def adx(self, data: Dict[str, Any], period: int = 14) -> float:
        """
        Calculate the Average Directional Index (ADX) over a specified period.

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            period (int): Period for the ADX calculation.

        Returns:
            float: Average Directional Index (ADX).
        """
        if len(data['High']) < period or len(data['Low']) < period:
            return 0  # Return 0 if there are not enough data points

        tr = [max(data['High'][i] - data['Low'][i],
                  abs(data['High'][i] - data['Close'][i - 1]),
                  abs(data['Low'][i] - data['Close'][i - 1])) for i in
              range(1, period + 1)]

        dm_plus = [
            data['High'][i] - data['High'][i - 1] if (data['High'][i] - data['High'][i - 1]) > (
                    data['Low'][i - 1] - data['Low'][i]) and (data['High'][i] - data['High'][
                i - 1]) > 0 else 0 for i in range(1, period + 1)]

        dm_minus = [data['Low'][i - 1] - data['Low'][i] if (data['Low'][i - 1] - data['Low'][i]) > (
                data['High'][i] - data['High'][i - 1]) and (data['Low'][i - 1] - data['Low'][
            i]) > 0 else 0 for i in range(1, period + 1)]

        tr_sum = np.sum(tr)
        if tr_sum == 0:
            return 0

        di_plus = (np.sum(dm_plus) / tr_sum) * 100
        di_minus = (np.sum(dm_minus) / tr_sum) * 100

        dx = (np.abs(di_plus - di_minus) / (di_plus + di_minus)) * 100
        return dx

    def adx_greater_than_x(self, data: Dict[str, Any], period: int = 14, x: float = 20) -> bool:
        """
        Check if the Average Directional Index (ADX) is greater than a specified value (x) over a specified period.

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            period (int): Period for the ADX calculation.
            x (float): Value to compare the ADX against.

        Returns:
            bool: True if the ADX is greater than x, False otherwise.
        """
        return self.adx(data, period) > x

    def di(self, data: Dict[str, Any], period: int = 14) -> tuple:
        """
        Calculate the Directional Movement Indicators (DI) over a specified period.

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            period (int): Period for the DI calculation.

        Returns:
            tuple: A tuple containing DI Plus and DI Minus values.
        """
        if len(data['High']) < period or len(data['Low']) < period:
            return 0, 0

        tr = [max(data['High'][i] - data['Low'][i],
                  abs(data['High'][i] - data['Close'][i - 1]),
                  abs(data['Low'][i] - data['Close'][i - 1])) for i in
              range(1, period + 1)]

        dm_plus = [
            data['High'][i] - data['High'][i - 1] if (data['High'][i] - data['High'][i - 1]) > (
                    data['Low'][i - 1] - data['Low'][i]) and (data['High'][i] - data['High'][
                i - 1]) > 0 else 0 for i in range(1, period + 1)]

        dm_minus = [data['Low'][i - 1] - data['Low'][i] if (data['Low'][i - 1] - data['Low'][i]) > (
                data['High'][i] - data['High'][i - 1]) and (data['Low'][i - 1] - data['Low'][
            i]) > 0 else 0 for i in range(1, period + 1)]

        tr_sum = np.sum(tr)
        if tr_sum == 0:
            return 0, 0

        di_plus = (np.sum(dm_plus) / tr_sum) * 100
        di_minus = (np.sum(dm_minus) / tr_sum) * 100

        return di_plus, di_minus

    def di_plus_above_x(self, data: Dict[str, Any], period: int = 13, x: float = 20) -> bool:
        """
        Check if the Directional Movement Indicator Plus (DI Plus) is above a specified value (x) over a specified period.

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            period (int): Period for the DI calculation.
            x (float): Value to compare the DI Plus against.

        Returns:
            bool: True if the DI Plus is above x, False otherwise.
        """
        di_plus, _ = self.di(data, period)
        return di_plus > x

    def di_minus_below_x(self, data: Dict[str, Any], period: int = 13, x: float = 20) -> bool:
        """
        Check if the Directional Movement Indicator Minus (DI Minus) is below a specified value (x) over a specified period.

        Args:
            data (Dict[str, Any]): Dictionary containing market data.
            period (int): Period for the DI calculation.
            x (float): Value to compare the DI Minus against.

        Returns:
            bool: True if the DI Minus is below x, False otherwise.
        """
        _, di_minus = self.di(data, period)
        return di_minus < x
