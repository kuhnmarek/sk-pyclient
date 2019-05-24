
import logging
import asyncio


class SKRemoteTaskService:
    def __init__(self, http_session, loop):

        self.logger = logging.getLogger('root')
        self.httpSession = http_session
        self.loop = loop
        self.url = None
        self.pipelineId = None

    def start_parallel(self, tasks):
        self.logger.info("Starting x tasks")

        return asyncio.run(self.async_start_parallell(tasks))

    async def async_start_parallell(self, tasks):
        async_tasks = []

        await self.httpSession.close()

        self.httpSession.new_session()

        for t in tasks:
            async_tasks.append(t.start(self.httpSession))

        await asyncio.gather(*async_tasks)

        results = [task.result for task in tasks]
        return results

