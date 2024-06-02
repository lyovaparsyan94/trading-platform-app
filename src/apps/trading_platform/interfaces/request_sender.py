from abc import ABC, abstractmethod

import requests


class RequestSender(ABC):

    @abstractmethod
    def make_request(self, url: str, headers: dict[str, str], data: dict) -> requests.Response:
        raise NotImplementedError
