import copy

default = {
    "ID": "",
}


def deserialize(data):
    """
    Parse data into Metrics.
    """
    metrics = []
    for d in data:
        m = Metric()
        m._Metric__data = data
        m.ID = d["ID"]
    return metrics


def serialize(metrics):
    """
    Dump Metrics as data.
    """
    data = []
    for m in metrics:
        d = copy.deepcopy(mc._Metric__data)
        d["ID"] = m.ID
        data.append(d)
    return data
    

class Metric(object):
    """
    Wraps a single Metric object.
    """
    def __init__(self, ID=""):
        self.__data = copy.deepcopy(default)
        self.ID = ID
