import copy

import metrics
import query as mquery


default = {
    "Description": "",
    "ID": "",
    "Metrics": [
        copy.deepcopy(metrics.default),
    ],
    "Name": "",
    "Query": copy.deepcopy(mquery.default),
}


def deserialize(data):
    """
    Parse data into MetricConfigs.
    """
    metricconfigs = []
    for d in data:
        mc = MetricConfig()
        mc._MetricConfig__data = d
        mc.name = d.get("Name")
        mc.ID = d.get("ID")
        mc.description = d.get("Description")
        mc.metrics = metrics.deserialize(d.get("Metrics", []))
        mc.query = mquery.deserialize(d.get("Query"))
        metricconfigs.append(mc)
    return metricconfigs


def serialize(metricconfigs):
    """
    Dump MetricConfigs as data.
    """
    data = []
    for mc in metricconfigs:
        d = copy.deepcopy(mc._MetricConfig__data)
        d["ID"] = mc.ID
        d["Name"] = mc.name
        d["Description"] = mc.description
        d["Metrics"] = metrics.serialize(mc.metrics)
        d["Query"] = mquery.serialize(mc.query)
        data.append(d)
    return data
    

class MetricConfig(object):
    """
    Wraps a single MetricConfig object.
    """
    def __init__(self, ID="", name="", description="", metrics=None,
                 query=None):
        self.__data = copy.deepcopy(default)
        self.ID = ID
        self.name = name
        self.description = description
        self.metrics = metrics or []
        self.query = query or mquery.Query()
