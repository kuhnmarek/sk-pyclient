
import asyncio

from utils.HttpSession import HttpSession


class SpaceKnowHttpSession(HttpSession):
    """A class to add SpaceKnow specifics to the http session (like headers and login mechanism)"""

    GET_JWT_TOKEN_URL = "https://spaceknow.auth0.com/oauth/ro"
    AUTHORIZE_USER_URL = "https://spaceknow-user.appspot.com/user/authorize"

    def __init__(self, loop):
        super().__init__()

        self.loop = loop
        self.jwt = ""
        self.headers = {'Content-Type': 'application/json'}

    def update_authorization_header(self, token_id):
        self.headers['Authorization'] = 'Bearer ' + token_id

    def login(self, credentials):
        """Logs user in using supplied credentials."""

        self.logger.info("Trying to log in")

        token = asyncio.run(self.post(self.GET_JWT_TOKEN_URL, credentials, ret_type="JSON"))
        self.update_authorization_header(token['id_token'])

        user = asyncio.run(self.post(self.AUTHORIZE_USER_URL,
                                     {"token": token['id_token']}, ret_type="JSON"))

        assert(user['authorized']), "Login error " + user
        self.logger.info("Logged in as:" + user['user']['name'])
