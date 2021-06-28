import requests_cache
from urllib3.exceptions import ReadTimeoutError

from src.exceptions.api_exceptions import ServiceNotAvailable
from src.services.service_abc import ServiceABC


class PatientDTO:
    def __init__(self, id_, name, email, phone):
        self.id = id_
        self.name = name
        self.email = email
        self.phone = phone


class PatientService(ServiceABC):
    def __init__(self, url: str):
        self.authorization = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGF0aWVudHMifQ.Pr6Z58GzNRtjX8Y09hEBzl7dluxsGiaxGlfzdaphzVU'
        self.headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': self.authorization}
        self._url = url
        self.session = requests_cache.CachedSession(expire_after=self.cache_ttl)

    @property
    def url(self):
        return self._url

    @property
    def cache_ttl(self):
        return 12

    @property
    def timeout(self):
        return 3

    @property
    def retry(self):
        return 2

    @property
    def path(self):
        return '/patients/'

    def get(self, patient_id: int):
        tries = self.retry
        while True:
            try:
                url = self.url + self.path + str(patient_id)
                content = self.session.get(url, headers=self.headers, timeout=self.timeout)
                json_content = self.validate_response(content)
                return PatientDTO(id_=json_content['id'], name=json_content['name'],
                                  email=json_content['email'], phone=json_content['phone'])
            except ReadTimeoutError:
                if tries > 0:
                    tries = tries - 1
                    continue
                raise ServiceNotAvailable()




