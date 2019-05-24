
"""
This is a tool to work with SpaceKnow imagery Platform using command line interface.


Currently it supports searching for imagery using Ragnar API and performing cars analysis through Kraken API.
Documentation for SpaceKnow Platform can be found at https://docs.spaceknow.com/


author: Marek Kuhn, 2019

"""

import asyncio
import argparse

import utils.file as files

from utils import log
from utils.SKHttpSession import SpaceKnowHttpSession as SKHttpSession
from utils.SKRemoteTaskService import SKRemoteTaskService

from core.CarsAnalysis import CarsAnalysis
from core.Imagery import Imagery


parser = argparse.ArgumentParser(description='Space Know command line client tool.')
requiredArgs = parser.add_argument_group('Required arguments')
requiredArgs.add_argument('-u', '--username', help='SpaceKnow account user name', required=True)
requiredArgs.add_argument('-p', '--password', help='SpaceKnow account password', required=True)
args = parser.parse_args()


logger = log.setup_logger('root')
loop = asyncio.get_event_loop()
http = SKHttpSession(loop)
tasking = SKRemoteTaskService(http, loop)


logger.info("Starting applicaton")
credentials = files.read_json("input/login.json")
credentials["username"] = args.username
credentials["password"] = args.password
http.login(credentials)


logger.info("Retrieving imagery")
imageryRequest = files.read_json("input/imagery_request.json")
imagery = Imagery(tasking, http)
scenes = imagery.get_scenes(imageryRequest)
if not scenes:
    logger.info("No imagery available, refine your search. Quitting.")
    quit()

# Clipping scenes for testing - remove to analyze all scenes
scenes = scenes[1:2]

logger.info("Starting cars analysis for {0} scenes".format(len(scenes)))
cars = CarsAnalysis(tasking, http)
cars.run(scenes, imageryRequest["extent"])
cars.download_results()

loop.run_until_complete(http.close())
