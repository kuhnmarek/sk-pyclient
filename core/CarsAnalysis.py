
from core.Analysis import Analysis
from utils.SKRemoteTask import SKRemoteTask


class CarsAnalysis(Analysis):

    URL_ANALYSIS = "https://spaceknow-kraken.appspot.com/kraken/release/cars/geojson"
    OUTPUT_FILES = (
        "cars.png",
        "trucks.png",
        "segmentation.ski",
        "detections.geojson",
        "area.json",
        "metadata.json"
    )

    def __init__(self, tasking_service, http):
        super().__init__(tasking_service, http)

    def create_task(self, scene, extent):
        return SKRemoteTask(self.URL_ANALYSIS, {"sceneId": scene["sceneId"], "extent": extent})



