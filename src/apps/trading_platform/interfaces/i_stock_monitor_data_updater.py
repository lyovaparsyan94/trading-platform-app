from abc import ABC, abstractmethod


class IStockMonitorDataUpdater(ABC):

    @abstractmethod
    def open_stockmonitor_page(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def login(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def go_filter_pages(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_data(self) -> None:
        raise NotImplementedError
