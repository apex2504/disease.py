import aiohttp
from .exceptions import NotFound, APIError

ver = "0.8.7"

class RequestClient:
    def __init__(self):
        self.session = aiohttp.ClientSession(headers={
            "User-Agent": "apex2504/python-corona-api v{}".format(ver)
        })

    async def make_request(self, endpoint, params=None):
        async with self.session.get(endpoint, params=params) as resp:
            if resp.status == 404:
                raise NotFound('No data available for specified country, state or province.')
            elif resp.status != 200:
                raise APIError('An unexpected error occurred.')
            
            return await resp.json()

    
    async def close(self):
        await self.session.close()