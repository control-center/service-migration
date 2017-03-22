import copy

import eventtags
import threshold as thresh

defaultType = "MinMax"

default = {
    "ID": "",
    "Name": "",
    "Description": "",
    "MetricSource" : "",
    "DataPoints": [],
    "Type": copy.deepcopy(defaultType),
    "Threshold": copy.deepcopy(thresh.default),
    "EventTags": copy.deepcopy(eventtags.default)
}

def deserialize(data):
    """
    Parse data into thresholdConfigs.
    """
    thresholdConfigs = []
    if not data:
        return thresholdConfigs
    for d in data:
        tc = ThresholdConfig()
        tc._ThresholdConfig__data = d
        for key, val in d.iteritems():
            if key == "ID":
                tc.thresholdID = val
            elif key == "Name":
                tc.name = val
            elif key == "Description":
                tc.description = val
            elif key == "MetricSource":
                tc.metricSource = val
            elif key == "DataPoints":
                tc.datapoints = val
            elif key == "Type":
                tc.thresholdType = val
            elif key == "Threshold":
                tc.threshold = thresh.deserialize(val)
            elif key == "EventTags":
                tc.eventTags = eventtags.deserialize(val)
        thresholdConfigs.append(tc)

    return thresholdConfigs

def serialize(thresholdConfigs):
    """
    Dump thresholdConfigs as data.
    """
    data = []
    for tc in thresholdConfigs:
        d = copy.deepcopy(tc._ThresholdConfig__data)
        d["ID"] = tc.thresholdID
        d["Name"] = tc.name
        d["Description"] = tc.description
        d["MetricSource"] = tc.metricSource
        d["DataPoints"] = tc.datapoints
        d["Type"] = tc.thresholdType
        d["Threshold"] = thresh.serialize(tc.threshold)
        d["EventTags"] = eventtags.serialize(tc.eventTags)
        data.append(d)

    return data


class ThresholdConfig(object):
    """
    Wraps a single ThresholdConfig object.
    """
    def __init__(self, thresholdID="", name="", description="", metricSource="",
                 datapoints=[], thresholdType=None, threshold=None, eventTags=None):
        self.__data = copy.deepcopy(default)
        self.thresholdID = thresholdID
        self.name = name
        self.description = description
        self.metricSource = metricSource
        self.datapoints = datapoints
        self.thresholdType = thresholdType or copy.deepcopy(defaultType)
        self.threshold = threshold or copy.deepcopy(thresh.default)
        self.eventTags = eventTags or copy.deepcopy(eventtags.default)
