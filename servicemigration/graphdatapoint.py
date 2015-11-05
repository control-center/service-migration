import copy

default = {
    "aggregator": "sum",
    "color": "",
    "expression": "",
    "fill": False,
    "format": "%d",
    "id": "",
    "legend": "",
    "metric": "",
    "metricSource": "r",
    "name": "",
    "rate": False,
    "rateOptions": None,
    "type": "line",
}


def deserialize(data):
    """
    Parse data into GraphDatapoints.
    """
    if not data:
        return []
    datapoints = []
    for d in data:
        p = GraphDatapoint()
        p._GraphDatapoint__data = d
        p.pointID = d["id"]
        p.name = d.get("name")
        p.aggregator = d.get("aggregator")
        p.color = d.get("color")
        p.expression = d.get("expression")
        p.fill = d.get("fill", False)
        p.dataFormat = d.get("dataFormat")
        p.legend = d.get("legend")
        p.metric = d.get("metric")
        p.metricSource = d.get("metricSource")
        p.rate = d.get("rate", False)
        p.rateOptions = d.get("rateOptions")
        p.pointType = d.get("pointType")
        datapoints.append(p)
    return datapoints


def serialize(datapoints):
    """
    Dump GraphDatapoints as data.
    """
    if not datapoints:
        return []
    data = []
    for p in datapoints:
        d = copy.deepcopy(p._GraphDatapoint__data)
        d["id"] = p.pointID
        d["name"] = p.name
        d["aggregator"] = p.aggregator
        d["color"] = p.color
        d["expression"] = p.expression
        d["fill"] = p.fill
        d["dataFormat"] = p.dataFormat
        d["legend"] = p.legend
        d["metric"] = p.metric
        d["metricSource"] = p.metricSource
        d["rate"] = p.rate
        d["rateOptions"] = p.rateOptions
        d["pointType"] = p.pointType
        data.append(d)
    return data
    

class GraphDatapoint(object):
    """
    Wraps a single GraphDatapoint object.
    """
    def __init__(self, pointID="", name="", aggregator="", color="",
                 expression="", fill=False, dataFormat="", legend="",
                 metric="", metricSource="", rate=False, rateOptions=None,
                 pointType=""):
        self.__data = copy.deepcopy(default)
        self.pointID = pointID
        self.name = name
        self.aggregator = aggregator
        self.color = color
        self.expression = expression
        self.fill = fill
        self.dataFormat = dataFormat
        self.legend = legend
        self.metric = metric
        self.metricSource = metricSource
        self.rate = rate
        self.rateOptions = rateOptions
        self.pointType = pointType
