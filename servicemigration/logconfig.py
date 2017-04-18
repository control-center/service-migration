import copy

import logtag


default = {
    "Path": "",
    "Type": "",
    "Filters": [],
    "LogTags": [
        copy.deepcopy(logtag.default),
        ],
    "IsAudit": True,
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
        lc.path = d.get("Path", default["Path"])
        lc.logType = d.get("Type", default["Type"])
        lc.filters = d.get("Filters", default["Filters"])
        lc.logTags = logtag.deserialize(d.get("LogTags", default["LogTags"]))
        lc.isAudit = d.get("IsAudit", default["IsAudit"])
        logconfigs.append(lc)
    return logconfigs


def serialize(logconfigs):
    """
    Serialize a list of LogConfig entities.
    """
    data = []
    for lc in logconfigs:
        d = copy.deepcopy(lc._LogConfig__data)
        d["Path"] = lc.path
        d["Type"] = lc.logType
        d["Filters"] = lc.filters
        d["LogTags"] = logtag.serialize(lc.logTags)
        d["IsAudit"] = lc.isAudit
        data.append(d)
    return data


class LogConfig(object):
    """
    A collection of path and type info, filters, and tags.
    """

    def __init__(self, path="", logType="", filters=None, logTags=None, isAudit=True):
        self.__data = copy.deepcopy(default)
        self.path = path
        self.logType = logType
        self.filters = filters or []
        self.logTags = logTags or []
        self.isAudit = isAudit
