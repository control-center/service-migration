import copy

default = {
    "Script": "",
    "Interval": 0,
    "Timeout": 0,
    "KillCountLimit": 0,
    "KillExitCodes": [],
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
        hc.kill_count_limit = v.get("KillCountLimit", default["KillCountLimit"])
        hc.kill_exit_codes = v.get("KillExitCodes", default["KillExitCodes"])
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
        data[hc.name]["KillCountLimit"] = hc.kill_count_limit
        data[hc.name]["KillExitCodes"] = hc.kill_exit_codes
    return data


class HealthCheck(object):
    """
    Wraps a single service healthcheck.
    """

    def __init__(self, name="", script="", interval=0, timeout=0, kill_count_limit=default["KillCountLimit"],
                 kill_exit_codes=None):
        self.__data = copy.deepcopy(default)
        self.name = name
        self.script = script
        self.interval = interval
        self.timeout = timeout
        if kill_exit_codes:
            if not isinstance(kill_exit_codes, list):
                raise ValueError("kill_exit_codes must be a list of integers")
            for item in kill_exit_codes:
                if not isinstance(item, int):
                    raise ValueError("kill_exit_codes must be a list of integers")
            self.kill_exit_codes = kill_exit_codes
        else:
            self.kill_exit_codes = default["KillExitCodes"]
        self.kill_count_limit = kill_count_limit


