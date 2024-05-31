from abc import ABC, abstractmethod

import requests


class RequestSender(ABC):
    @abstractmethod
    def get_headers(self, cookies: dict[str, str]) -> dict[str, str]:
        raise NotImplementedError

    @abstractmethod
    def make_request(self, url: str, stock_count: int, headers: dict[str, str], payload: dict, dir_: str) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def first_request(self, url: str, payload: dict, headers: dict[str, str]) -> requests.Response:
        raise NotImplementedError

    @abstractmethod
    def second_request(self, url: str, payload: dict, headers: dict[str, str]) -> requests.Response:
        raise NotImplementedError
