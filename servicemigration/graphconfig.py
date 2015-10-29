import copy

import graphdatapoint
import graphrange


default = {
    "id": "",
    "datapoints": [
        copy.deepcopy(graphdatapoint.default),
    ],
    "base": 0,
    "builtin": False,
    "description": "",
    "footer": False,
    "format": "",
    "id": "",
    "maxy": None,
    "miny": None,
    "name": "",
    "range": copy.deepcopy(graphrange.default),
    "returnset": "",
    "tags": {},
    "type": "",
    "units": "",
    "yAxisLabel": "",
}


def deserialize(data):
    """
    Parse data into GraphConfigs.
    """
    graphconfigs = []
    for d in data:
        gc = GraphConfig()
        gc._GraphConfig__data = d
        gc.graphID = d["id"]
        gc.name = d.get("name")
        gc.description = d.get("description")
        gc.datapoints = graphdatapoint.deserialize(d.get("datapoints", []))
        gc.graphRange = graphrange.deserialize(d.get("range", {}))
        gc.base = d.get("base")
        gc.builtin = d.get("builtin")
        gc.footer = d.get("footer")
        gc.graphFormat = d.get("format")
        gc.maxy = d.get("maxy")
        gc.miny = d.get("miny")
        gc.returnset = d.get("returnset")
        gc.tags = d.get("tags", {})
        gc.graphType = d.get("type")
        gc.units = d.get("units")
        gc.yAxisLabel = d.get("yAxisLabel")
        graphconfigs.append(gc)
    return graphconfigs


def serialize(graphconfigs):
    """
    Dump GraphConfigs as data.
    """
    data = []
    for gc in graphconfigs:
        d = copy.deepcopy(gc._GraphConfig__data)
        d["id"] = gc.graphID
        d["datapoints"] = graphdatapoint.serialize(gc.datapoints)
        d["range"] = graphrange.serialize(gc.graphRange)
        d["base"] = gc.base
        d["builtin"] = gc.builtin
        d["description"] = gc.description
        d["footer"] = gc.footer
        d["format"] = gc.graphFormat
        d["maxy"] = gc.maxy
        d["miny"] = gc.miny
        d["name"] = gc.name
        d["returnset"] = gc.returnset
        d["tags"] = gc.tags
        d["type"] = gc.graphType
        d["units"] = gc.units
        d["yAxisLabel"] = gc.yAxisLabel
        data.append(d)
    return data
    

class GraphConfig(object):
    """
    Wraps a single GraphConfig object.
    """
    def __init__(self, graphID="", name="", description="", datapoints=None,
                 graphRange=None, base=0, builtin=False, footer=False,
                 graphFormat="", miny=None, maxy=None, returnset="", tags=None,
                 graphType="", units="", yAxisLabel=""):
        self.__data = copy.deepcopy(default)
        self.graphID = graphID
        self.name = name
        self.description = description
        self.datapoints = datapoints or []
        self.graphRange = graphRange or graphrange.GraphRange()
        self.base = base
        self.builtin = builtin
        self.footer = footer
        self.graphFormat = graphFormat
        self.miny = miny
        self.maxy = maxy
        self.returnset = returnset
        self.tags = tags or {}
        self.graphType = graphType
        self.units = units
        self.yAxisLabel = yAxisLabel
