
import logging
import asyncio


class SKRemoteTask:
    """A class to represent a task (pipeline) to remote SpaceKnow server"""

    TASKING_API_URL = "https://spaceknow-tasking.appspot.com/tasking/get-status"

    def __init__(self, url, request_data):
        self.logger = logging.getLogger('root')

        self.url = url
        self.request_data = request_data

        self.pipelineId = None
        self.nextTry = 0
        self.httpSession = None
        self.result = None

    async def start(self, http_session):
        """Starts the task by calling /initiate. Saves the pipelineId."""

        self.logger.info("Starting task")
        self.httpSession = http_session

        response = await self.httpSession.post(self.url + "/initiate", self.request_data, ret_type="JSON")

        assert("status" in response and response["status"] == "NEW"), "Remote task initiate failed"
        self.logger.info("Remote task initiated, pipeline id: " + response["pipelineId"])

        self.pipelineId = response["pipelineId"]
        self.nextTry = response["nextTry"]

        await self.get_status()

    async def get_status(self):
        """Periodically checks the status of the task using Tasking API. Calls retrieve when it's done."""

        while True:
            self.logger.info("Task " + self.pipelineId + " waiting " + str(self.nextTry) + " s")
            await asyncio.sleep(self.nextTry)

            response = await self.httpSession.post(self.TASKING_API_URL, {"pipelineId": self.pipelineId}, ret_type="JSON")

            if response["status"] == "RESOLVED":
                break
            else:
                assert(response["status"] == "PROCESSING"), "Remote task has some unexpected status"

            self.nextTry = response["nextTry"]
            self.logger.info("Task " + self.pipelineId + " status: " + response["status"])

        await self.retrieve()

    async def retrieve(self):
        """Retrieves the task result after the task is resolved. """

        response = await self.httpSession.post(self.url + "/retrieve", {"pipelineId": self.pipelineId}, ret_type="JSON")
        self.result = response
