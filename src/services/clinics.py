import requests_cache
from urllib3.exceptions import ReadTimeoutError

from src.exceptions.api_exceptions import ServiceNotAvailable
from src.services.service_abc import ServiceABC


class ClinicDTO:
    def __init__(self, id_, name):
        self.id = id_
        self.name = name


class ClinicService(ServiceABC):
    def __init__(self, url: str):
        self.authorization = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoiY2xpbmljcyJ9.r3w8KS4LfkKqZhOUK8YnIdLhVGJEqnReSClLCMBIJRQ'
        self.headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': self.authorization}
        self._url = url
        self.session = requests_cache.CachedSession(expire_after=self.cache_ttl)

    @property
    def url(self):
        return self._url

    @property
    def cache_ttl(self):
        return 72

    @property
    def timeout(self):
        return 5

    @property
    def retry(self):
        return 2

    @property
    def path(self):
        return '/clinics/'

    def get(self, clinic_id: int) -> ClinicDTO:
        tries = self.retry
        while True:
            url = self.url + self.path + str(clinic_id)
            try:
                content = self.session.get(url, headers=self.headers, timeout=self.timeout)
                json_content = self.validate_response(content)
                return ClinicDTO(id_=json_content['id'], name=json_content['name'])
            except ReadTimeoutError:
                if tries > 0:
                    tries = tries - 1
                    continue
                raise ServiceNotAvailable()




