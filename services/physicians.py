import requests
from services.service_abc import ServiceABC


class PhysiciansDTO:
    def __init__(self, id_, name, crm):
        self.id = id_
        self.name = name
        self.crm = crm


class PhysiciansService(ServiceABC):
    def __init__(self):
        self.authorization = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA'
        self.headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': self.authorization}

    @property
    def url(self):
        return 'https://5f71da6964a3720016e60ff8.mockapi.io/v1'

    @property
    def cache_ttl(self):
        return 48

    @property
    def timeout(self):
        return 4

    @property
    def retry(self):
        return 2

    @property
    def path(self):
        return '/physicians/'

    def get(self, patient_id: str):
        url = self.url + self.path + patient_id
        content = requests.get(url, headers=self.headers, timeout=self.timeout)
        json_content = self.validate_response(content)
        return PhysiciansDTO(id_=json_content['id'], name=json_content['name'],
                             crm=json_content['crm'])



