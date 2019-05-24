
import asyncio

from utils.HttpSession import HttpSession


class SpaceKnowHttpSession(HttpSession):

    def __init__(self, loop):
        super().__init__()

        self.loop = loop
        self.jwt = ""
        self.headers = {'Content-Type': 'application/json'}

    def update_authorization_header(self, token_id):
        self.headers['Authorization'] = 'Bearer ' + token_id

    def login(self, credentials):
        # todo reuse existing session
        self.logger.info("Trying to log in")

        token = asyncio.run(self.post("https://spaceknow.auth0.com/oauth/ro", credentials, ret_type="JSON"))
        self.update_authorization_header(token['id_token'])

        user = asyncio.run(self.post("https://spaceknow-user.appspot.com/user/authorize",
                                     {"token": token['id_token']}, ret_type="JSON"))

        assert(user['authorized']), "Login error " + user
        self.logger.info("Logged in as:" + user['user']['name'])
