
import logging

from utils.SKRemoteTask import SKRemoteTask


class Imagery:

    IMAGERY_URL = "https://spaceknow-imagery.appspot.com/imagery/search"

    def __init__(self, tasking_service, http):
        self.logger = logging.getLogger('root')
        self.taskingService = tasking_service
        self.http = http
        self.result = None

    def get_scenes(self, data):

        task = SKRemoteTask(self.IMAGERY_URL, data)
        self.result = self.taskingService.start_parallel([task])

        assert(self.result[0]['cursor'] is None), "Paginated response NOT SUPPORTED now."

        return self.result[0]["results"]
