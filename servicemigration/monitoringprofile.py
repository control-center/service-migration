import copy

import metricconfig
import graphconfig
import thresholdconfig


default = {
    "MetricConfigs": [
        copy.deepcopy(metricconfig.default)
    ],
    "GraphConfigs": [
        copy.deepcopy(graphconfig.default)
    ],
    "ThresholdConfigs": [
        copy.deepcopy(thresholdconfig.default)
    ]
}


def deserialize(data):
    """
    Parse data into a MonitoringProfile.
    """
    mp = MonitoringProfile()
    mp._MonitoringProfile__data = data
    mp.metricConfigs = metricconfig.deserialize(data.get("MetricConfigs", []))
    mp.graphConfigs = graphconfig.deserialize(data.get("GraphConfigs", []))
    mp.thresholdConfigs = thresholdconfig.deserialize(data.get("ThresholdConfigs", []))
    return mp


def serialize(monpro):
    """
    Dump a MonitoringProfile as data.
    """
    data = copy.deepcopy(monpro._MonitoringProfile__data)
    data["MetricConfigs"] = metricconfig.serialize(monpro.metricConfigs)
    data["GraphConfigs"] = graphconfig.serialize(monpro.graphConfigs)
    data["ThresholdConfigs"] = thresholdconfig.serialize(monpro.thresholdConfigs)
    return data


class MonitoringProfile(object):
    """
    """
    def __init__(self, metricConfigs=None, graphConfigs=None, thresholdConfigs=None):
        self.__data = copy.deepcopy(default)
        self.metricConfigs = metricConfigs or []
        self.graphConfigs = graphConfigs or []
        self.thresholdConfigs = thresholdConfigs or []
