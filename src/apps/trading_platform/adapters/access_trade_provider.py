
import pandas
import pandas_market_calendars as market_calendar

from src.apps.trading_platform.interfaces.access_trade_provider import IAccessTradeProvider


class AccessTradeProvider(IAccessTradeProvider):

    def has_access_now(self) -> bool:
        calendar = market_calendar.get_calendar("NYSE")
        now = pandas.Timestamp.utcnow()
        print(now)
        schedule = calendar.schedule(start_date=now.strftime('%Y-%m-%d'), end_date=now.strftime('%Y-%m-%d'))

        if schedule.empty:
            return False

        print(schedule)

        market_open = schedule.iloc[0]['market_open']
        market_close = schedule.iloc[0]['market_close']

        return market_open <= now <= market_close
