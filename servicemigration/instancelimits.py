import copy

_default = {
   "Min": 1,
   "Max": 0,
   "Default": 0
}

def deserialize(data):
    """
    Deserializes an InstanceLimits
    """
    il = InstanceLimits()
    il.__InstanceLimits_data = data
    il.minimum = data.get("Min", 1)
    il.maximum = data.get("Max", 0)
    il.default = data.get("Default", 0)
    return il

def serialize(il):
    """
    Serializes an InstanceLimits.
    """
    data = copy.deepcopy(il.__InstanceLimits_data)
    data["Min"] = il.minimum
    data["Max"] = il.maximum
    data["Default"] = il.default
    return data

class InstanceLimits:
    """
    Wraps a single InstanceLimits
    """
    def __init__(self, minimum=1, maximum=0, default=0):
        self.__data = copy.deepcopy(_default)
        self.minimum = minimum
        self.maximum = maximum
        self.default = default