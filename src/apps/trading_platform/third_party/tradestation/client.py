from abc import ABC, abstractmethod
from typing import Any, Literal

from requests import request

Method = Literal[
    "GET",
    "POST",
    "PUT",
]


class TradeStationHTTPClient(ABC):

    @abstractmethod
    def request(
        self,
        url: str,
        method: Method = "GET",
        params: dict | None = None,
        json: dict | list | None = None,
        headers: dict | None = None,
        cookies: dict | None = None,
        data: Any | None = None,
    ) -> Any:
        raise NotImplementedError


class RequestsTradeStationHTTPClient(TradeStationHTTPClient):

    def __init__(self, proxy: str):
        self.proxy = proxy

    def request(
        self,
        url: str,
        method: Method = "GET",
        params: dict | None = None,
        json: dict | list | None = None,
        headers: dict | None = None,
        cookies: dict | None = None,
        data: Any | None = None,
    ) -> Any:
        response = request(
            method=method,
            params=params,
            url=url,
            json=json,
            headers=headers,
            cookies=cookies,
            data=data,
            # proxies=self.proxy,
        )
        print(response.text)
        response.raise_for_status()
        return response.json()
