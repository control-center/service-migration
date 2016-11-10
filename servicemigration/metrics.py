import copy

default = {
    "ID": "",
    "Name": "",
    "Description": "",
    "Unit": "",
    "Counter": False,
    "ResetValue": 0,
    "BuiltIn": False,
}


def deserialize(data):
    """
    Parse data into Metrics.
    """
    metrics = []
    if not data:
        return metrics
    for d in data:
        m = Metric()
        m._Metric__data = d
        m.ID = d.get("ID", "")
        m.name = d.get("Name")
        m.description = d.get("Description")
        m.unit = d.get("Unit")
        m.counter = d.get("Counter", False)
        m.resetValue = d.get("ResetValue", 0)
        m.builtin = d.get("Builtin", False)
        metrics.append(m)
    return metrics


def serialize(metrics):
    """
    Dump Metrics as data.
    """
    data = []
    if not metrics:
        return data
    for m in metrics:
        d = copy.deepcopy(m._Metric__data)
        d["ID"] = m.ID
        d["Name"] = m.name
        d["Description"] = m.description
        d["Unit"] = m.unit
        d["Counter"] = m.counter
        d["ResetValue"] = m.resetValue
        d["BuiltIn"] = m.builtin
        data.append(d)
    return data
    

class Metric(object):
    """
    Wraps a single Metric object.
    """
    def __init__(self, ID="", name="", description="", unit="", counter=False,
                 resetValue=0, builtin=False):
        self.__data = copy.deepcopy(default)
        self.ID = ID
        self.name = name
        self.description = description
        self.unit = unit
        self.counter = counter
        self.resetValue = resetValue
        self.builtin = builtin
