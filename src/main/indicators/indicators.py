class IndicatorCalculator:
    def __init__(self, data):
        self.data = data

    def high_decreasing(self, period=3):
        return all(self.data['High'][i] < self.data['High'][i - 1] for i in range(-period, 0))

    def close_greater_than_high(self):
        return self.data['Close'][-1] > self.data['High'][-2]

    def close_greater_than_x(self, x):
        return self.data['Close'][-1] > x

    def volume_greater_than_x(self, x):
        return self.data['Volume'][-1] > x

    def ma(self, period):
        return sum(self.data['Close'][-period:]) / period

    def wma(self, period):
        weights = list(range(1, period + 1))
        weighted_sum = sum(self.data['Close'][-i] * weights[-i] for i in range(1, period + 1))
        return weighted_sum / sum(weights)

    def ma_greater_than_wma(self, ma_period=9, wma_period=5):
        return self.ma(ma_period) > self.wma(wma_period)

    def rsi(self, period=14):
        gains = []
        losses = []
        for i in range(1, period + 1):
            change = self.data['Close'][-i] - self.data['Close'][-i - 1]
            if change > 0:
                gains.append(change)
            else:
                losses.append(abs(change))
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def rsi_crossed_above(self, period=14, x=30):
        prev_rsi = self.rsi(period - 1)
        curr_rsi = self.rsi(period)
        return prev_rsi < x < curr_rsi

    def rsi_greater_than_x(self, period=14, x=70):
        return self.rsi(period) > x

    def close_crossed_above_ma(self, ma_period=9):
        ma_value = self.ma(ma_period)
        return self.data['Close'][-2] < ma_value < self.data['Close'][-1]

    def cci(self, period=14, constant=0.015):
        tp = [(self.data['High'][i] + self.data['Low'][i] + self.data['Close'][i]) / 3 for i in range(-period, 0)]
        ma_tp = sum(tp) / period
        mean_deviation = sum(abs(tp_i - ma_tp) for tp_i in tp) / period
        if mean_deviation == 0:
            return 0
        return (tp[-1] - ma_tp) / (constant * mean_deviation)

    def cci_greater_than_x(self, period=14, x=100):
        return self.cci(period) > x

    def aroon(self, period=25):
        aroon_up = ((period - (self.data['High'][-period:].index(max(self.data['High'][-period:]))) - 1) / period) * 100
        aroon_down = ((period - (self.data['Low'][-period:].index(min(self.data['Low'][-period:]))) - 1) / period) * 100
        return aroon_up, aroon_down

    def aroon_up_greater_than_x(self, period=25, x=70):
        aroon_up, _ = self.aroon(period)
        return aroon_up > x

    def aroon_down_less_than_x(self, period=25, x=30):
        _, aroon_down = self.aroon(period)
        return aroon_down < x

    def ma3_greater_than_ma9(self):
        return self.ma(3) > self.ma(9)

    def adx(self, period=14):
        tr = []
        dm_plus = []
        dm_minus = []
        for i in range(1, period + 1):
            tr.append(max(self.data['High'][-i] - self.data['Low'][-i],
                          abs(self.data['High'][-i] - self.data['Close'][-i - 1]),
                          abs(self.data['Low'][-i] - self.data['Close'][-i - 1])))
            dm_plus.append(
                max(self.data['High'][-i] - self.data['High'][-i - 1], 0) if self.data['High'][-i] - self.data['High'][
                    -i - 1] > self.data['Low'][-i - 1] - self.data['Low'][-i] else 0)
            dm_minus.append(
                max(self.data['Low'][-i - 1] - self.data['Low'][-i], 0) if self.data['Low'][-i - 1] - self.data['Low'][
                    -i] > self.data['High'][-i] - self.data['High'][-i - 1] else 0)

        tr_sum = sum(tr)
        if tr_sum == 0:
            return 0

        di_plus = (sum(dm_plus) / tr_sum) * 100
        di_minus = (sum(dm_minus) / tr_sum) * 100

        dx = (abs(di_plus - di_minus) / (di_plus + di_minus)) * 100
        return sum(dx for _ in range(period)) / period

    def adx_greater_than_x(self, period=14, x=20):
        return self.adx(period) > x

    def di(self, period=14):
        tr = []
        dm_plus = []
        dm_minus = []
        for i in range(1, period + 1):
            tr.append(max(self.data['High'][-i] - self.data['Low'][-i],
                          abs(self.data['High'][-i] - self.data['Close'][-i - 1]),
                          abs(self.data['Low'][-i] - self.data['Close'][-i - 1])))
            dm_plus.append(
                max(self.data['High'][-i] - self.data['High'][-i - 1], 0) if self.data['High'][-i] - self.data['High'][
                    -i - 1] > self.data['Low'][-i - 1] - self.data['Low'][-i] else 0)
            dm_minus.append(
                max(self.data['Low'][-i - 1] - self.data['Low'][-i], 0) if self.data['Low'][-i - 1] - self.data['Low'][
                    -i] > self.data['High'][-i] - self.data['High'][-i - 1] else 0)
        tr_sum = sum(tr)
        if tr_sum == 0:
            return 0, 0
        di_plus = (sum(dm_plus) / tr_sum) * 100
        di_minus = (sum(dm_minus) / tr_sum) * 100
        return di_plus, di_minus

    def di_plus_above_x(self, period=13, x=20):
        di_plus, _ = self.di(period)
        return di_plus > x

    def di_minus_below_x(self, period=13, x=20):
        _, di_minus = self.di(period)
        return di_minus < x
