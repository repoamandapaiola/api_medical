import json
from abc import ABC, abstractmethod

from exceptions.api_exceptions import ServiceNotAvailable, NotFound


class ServiceABC(ABC):

    @property
    @abstractmethod
    def url(self):
        pass

    @property
    @abstractmethod
    def cache_ttl(self):
        pass

    @property
    @abstractmethod
    def timeout(self):
        pass

    @property
    @abstractmethod
    def retry(self):
        pass

    @property
    @abstractmethod
    def path(self):
        pass

    def validate_response(self, content):
        if content.status_code == 200:
            response = json.loads(content.content.decode())
            return response
        if 400 < content.status_code < 500:
            raise NotFound()
        if content.status_code >= 500:
            raise ServiceNotAvailable()
