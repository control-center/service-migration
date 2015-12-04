import copy

default = {
    "Script": "",
    "Interval": 0,
    "Timeout": 0
}

def deserialize(data):
    """
    Deserializes a list of HealthChecks.
    """
    healthchecks = []
    if data is None:
        return []
    for k, v in data.iteritems():
        hc = HealthCheck()
        hc._HealthCheck__data = v
        hc.name = k
        hc.script = v.get("Script", "")
        hc.interval = v.get("Interval", 0)
        hc.timeout = v.get("Timeout", 0)
        healthchecks.append(hc)
    return healthchecks

def serialize(healthchecks):
    """
    Serializes a list of healthchecks.
    """
    data = {}
    for hc in healthchecks:
        data[hc.name] = hc._HealthCheck__data
        data[hc.name]["Script"] = hc.script
        data[hc.name]["Interval"] = hc.interval
        data[hc.name]["Timeout"] = hc.timeout
    return data


class HealthCheck(object):
    """
    Wraps a single service healthcheck.
    """

    def __init__(self, name="", script="", interval=0, timeout=0):
        self.__data = copy.deepcopy(default)
        self.name = name
        self.script = script
        self.interval = interval
        self.timeout = timeout


