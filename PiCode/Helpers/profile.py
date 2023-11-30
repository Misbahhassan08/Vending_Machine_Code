import json
import ast
import Helpers.configuration as config
import Helpers.logger as logger

class Profile(object):
    def __init__(self):
        self.BrewProfileID = ""
        self.RootCompanyID = ""
        self.BrewProfileName = ""
        self.AbsorptionFactor = ""
        self.CoffeeOriginName = ""
        self.CoffeeGrinderName = ""
        self.CoffeeGrinderSetting = ""
        self.CoffeeWeight = ""
        self.PreInfuse = ""
        self.TargetFlowRate = ""
        self.ConcentrateYield = ""
        self.ConcenrateTotalDisolvedSolids = ""
        self.ReadyToDrinkTotalDisolvedSolids = ""
        self.IntervalMinutes = []
        self.BrewMinutes = ""
        self.RestMinutes = ""
        self.TotalMinutes = ""
    def GetIntervals(self):
        return ast.literal_eval(self.IntervalMinutes)
    def get(self, BrewProfileName):
        try:
            j = config.get_value("profiles", str(BrewProfileName))
            self.__dict__ = ast.literal_eval(j)
        except Exception as e:
            logger.error(str(e))
    def save(self):
        try:
            config.set_value("profiles", self.BrewProfileName, json.dumps(self.__dict__))
        except Exception as e:
            logger.error(str(e))
