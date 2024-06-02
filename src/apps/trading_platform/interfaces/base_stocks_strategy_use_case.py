from abc import ABC, abstractmethod


class BaseStocksStrategyUseCase(ABC):
    @abstractmethod
    def get_stocks_for_strategy(self, stock_count: int, strategy_name: str) -> list[str]:
        raise NotImplementedError

    def _relogin(self) -> None:
        raise NotImplementedError
