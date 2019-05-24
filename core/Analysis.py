
import os
import uuid

import utils.file as files

from utils.SKRemoteTask import *


class Analysis:
    """
    An abstract class to represent a SpaceKnow analysis i.e. a task to run a machine learning algorithm on supplied imagery.

    Also it collects and downloads the results.
    """

    PATH_DOWNLOAD_IMAGE = "data/img/"
    PATH_OUTPUT = "data/img/{0}/"

    # https://spaceknow-kraken.appspot.com/kraken/grid/< map_id >/< geometry_id >/< z >/< x >/< y >/< file_name >
    URL_GRID_IMAGERY =  "https://spaceknow-kraken.appspot.com/kraken/grid/{0}/{1}/{2}/{3}/{4}/{5}"

    def __init__(self, tasking_service, http):
        self.logger = logging.getLogger('root')
        self.http = http
        self.taskingService = tasking_service
        self.id = None
        self.result = None

    def run(self, scenes, extent):
        """Creates tasks for the specific analysis algorithm and starts them using Tasking service."""

        self.id = uuid.uuid4()      # Generate identifier for each analysis run - for file naming etc.

        tasks = []
        for s in scenes:
            tasks.append(self.create_task(s, extent))

        self.result = self.taskingService.start_parallel(tasks)

    def download_results(self):
        """Initiates the download of the result files."""
        # Make output folder for this run
        os.mkdir(self.PATH_OUTPUT.format(str(self.id)))

        # TODO change this for multiple scenes
        scene = self.result[0]
        asyncio.run(self.fetch_scene(scene))

    async def fetch_scene(self, scene):
        """Coroutine to fetch analysis results from the grid endpoint."""

        # TODO make parallel
        for output_file_name in self.OUTPUT_FILES:
            for i in range(len(scene['tiles'])):
                tile = scene['tiles'][i]

                url = self.URL_GRID_IMAGERY.format(
                    scene["mapId"],
                    "-",                   # geometry_id ignored for now
                    tile[0],
                    tile[1],
                    tile[2],
                    output_file_name
                )

                # TODO saving file one by one -> refactor, should be somewhere else
                response = await self.http.get_bytes(url)

                output_file_path = self.PATH_OUTPUT.format(self.id) + output_file_name + "_" + str(i)
                files.write_bytes(output_file_path, response)

                self.logger.info("Downloaded file " + output_file_path)
