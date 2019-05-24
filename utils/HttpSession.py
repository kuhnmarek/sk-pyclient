import aiohttp
import logging


class HttpSession:

    def __init__(self):
        self.logger = logging.getLogger('root')
        self.session = aiohttp.ClientSession()
        self.headers = {}

    async def post(self, url, data="", ret_type=None):
        self.logger.debug("POST " + url)

        async with aiohttp.ClientSession() as session:
            response = await session.post(url, json=data, headers=self.headers)

            assert (response.status == 200), \
                "Request failed: (" + str(response.status) + ") " + response.reason + " " + str(response.url) + " " + str(data) + str(response.headers)

            if ret_type is None:
                return response
            else:
                self.logger.debug("POST Response: " + str(response))
                if ret_type == "JSON":
                    try:
                        return await response.json()
                    except aiohttp.ContentTypeError:
                        self.logger.error("Invalid JSON response")
                        return {}

    async def get(self, url):
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers=self.headers)

        assert (response.status == 200), \
            "Request failed: (" + str(response.status) + ") " + response.reason + " " + str(response.url)

        self.logger.debug("GET Response: " + str(response))
        return response

    async def get_bytes(self, url):
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers=self.headers)

            assert (response.status == 200), \
                "Request failed: (" + str(response.status) + ") " + response.reason + " " + str(response.url)

            self.logger.debug("GET Response: " + str(response))
            return  await response.read()

    async def close(self):
        await self.session.close()

    def new_session(self):
        self.session = aiohttp.ClientSession()
