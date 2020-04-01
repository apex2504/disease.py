import aiohttp
from .exceptions import *

class RequestClient:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def make_request(self, endpoint):
        async with self.session.get(endpoint) as resp:
            if resp.status == 404:
                raise NotFound('No data available for specified country, state or province.')
            elif resp.status != 200:
                raise APIError('An unexpected error occurred.')
            
            return await resp.json()