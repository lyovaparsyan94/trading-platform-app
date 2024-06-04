class StockRepository:

    def __init__(self, data_source):
        self.data_source = data_source

    def save_stocks(self, account_name: str, strategy_type: str, stocks: list[str]) -> None:
        if account_name not in self.data_source:
            self.data_source[account_name] = {}
        self.data_source[account_name][strategy_type] = stocks

    def get_stocks(self, account_name: str, strategy_type: str) -> list[str]:
        return self.data_source.get(account_name, {}).get(strategy_type, [])

    def delete_stocks(self, account_name: str, strategy_type: str) -> None:
        if account_name in self.data_source and strategy_type in self.data_source[account_name]:
            del self.data_source[account_name][strategy_type]

