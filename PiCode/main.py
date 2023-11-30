#!/usr/bin/python3.7
import queue
import Helpers.APICall as APICall
import Helpers.menu as menu
import Helpers.logger as logger
from Helpers.GlobalFunctions import SetThreadName

def main():
    SetThreadName("Brew")
    MainQueue = queue.Queue() #Create an event queue for the main app
    APIQueue = queue.Queue() #Create an event queue for external API Calls
    logger.info("Brewer Application Starting")
    try:
        MenuThread = menu.Menu(MainQueue, APIQueue)
    except Exception as e:
        logger.error(e)
    try:
        APIThread = APICall.APICall(MainQueue, APIQueue)
    except Exception as e:
        logger.error(e)
    MenuThread.join()
    APIThread.join()
    logger.info("Brewer Application Ended")
main()
