import copy

import logtag


default = {
    "path": "",
    "type": "",
    "filters": [],
    "LogTags": [
        copy.deepcopy(logtag.default),
        ],
}


def deserialize(data):
    """
    Deserialize a list of LogConfig entities.
    """
    if not data:
        return []
    logconfigs = []
    for d in data:
        lc = LogConfig()
        lc._LogConfig__data = d
        lc.path = d.get("path", d.get("Path"))
        lc.logType = d.get("type", d.get("Type"))
        lc.filters = d.get("filters", d.get("Filters"))
        lc.logTags = logtag.deserialize(d.get("LogTags", []))
        logconfigs.append(lc)
    return logconfigs


def serialize(logconfigs):
    """
    Serialize a list of LogConfig entities.
    """
    data = []
    for lc in logconfigs:
        d = copy.deepcopy(lc._LogConfig__data)
        d["path"] = lc.path
        d["type"] = lc.logType
        d["filters"] = lc.filters
        d["LogTags"] = logtag.serialize(lc.logTags)
        data.append(d)
    return data


class LogConfig(object):
    """
    A collection of path and type info, filters, and tags.
    """

    def __init__(self, path="", logType="", filters=None, logTags=None):
        self.__data = copy.deepcopy(default)
        self.path = path
        self.logType = logType
        self.filters = filters or []
        self.logTags = logTags or []
