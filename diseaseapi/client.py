from .covid import Covid
from .influenza import Influenza
from .request import RequestClient

class Client:
    def __init__(self, base_url='https://disease.sh/v3'):
        request_client = RequestClient()
        self.base_url = base_url
        self.covid19 = Covid(base_url, request_client)
        self.influenza = Influenza(base_url, request_client)