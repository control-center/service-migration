import copy

import metricconfig
import graphconfig


default = {
    "MetricConfigs": [
        copy.deepcopy(metricconfig.default),
        ],
}


def deserialize(data):
    """
    Parse data into a MonitoringProfile.
    """
    mp = MonitoringProfile()
    mp._MonitoringProfile__data = data
    mp.metricConfigs = metricconfig.deserialize(data.get("MetricConfigs", []))
    mp.graphConfigs = graphconfig.deserialize(data.get("GraphConfigs", []))
    return mp


def serialize(monpro):
    """
    Dump a MonitoringProfile as data.
    """
    data = copy.deepcopy(monpro._MonitoringProfile__data)
    data["MetricConfigs"] = metricconfig.serialize(monpro.metricConfigs)
    data["GraphConfigs"] = graphconfig.serialize(monpro.graphConfigs)
    return data
    

class MonitoringProfile(object):
    """
    """
    def __init__(self, metricConfigs=None, graphConfigs=None):
        self.__data = copy.deepcopy(default)
        self.metricConfigs = metricConfigs or []
        self.graphConfigs = graphConfigs or []
