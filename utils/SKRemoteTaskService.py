
import logging
import asyncio


class SKRemoteTaskService:
    """This class manages SpaceKnow remote tasks in an asynchronous fashion."""

    def __init__(self, http_session, loop):
        self.logger = logging.getLogger('root')
        self.httpSession = http_session
        self.loop = loop
        self.url = None
        self.pipelineId = None

    def start_parallel(self, tasks):
        """Starts a number of SKRemoteTasks in parallel using asyncio.

        Parameters
        ----------
        tasks : list<SKRemoteTask>
        """

        return asyncio.run(self.async_start_parallel(tasks))

    async def async_start_parallel(self, tasks):
        """Coroutine to collect tasks and gather results"""

        async_tasks = []

        for t in tasks:
            async_tasks.append(t.start(self.httpSession))

        await asyncio.gather(*async_tasks)

        results = [task.result for task in tasks]
        return results

