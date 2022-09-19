

class BaseService:
    api_url: str

    def __init__(self, api_url):
        self.api_url = api_url
