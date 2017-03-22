import copy

default = {
    "Min": "",
    "Max": ""
}

def deserialize(data):
    """
    Parse data into a Threshold object.
    """
    threshold = Threshold()
    threshold._Threshold__data = data
    for key, val in data.iteritems():
        if key == "Min":
            threshold.min = val
        elif key == "Max":
            threshold.max = val

    return threshold

def serialize(threshold):
    """
    Dump threshold as data.
    """
    d = copy.deepcopy(threshold._Threshold__data)
    d["Min"] = threshold.min
    d["Max"] = threshold.max

    return d

class Threshold(object):
    """
    Wraps a single Threshold object.
    """
    def __init__(self, thresholdMin="", thresholdMax=""):
        self.__data = copy.deepcopy(default)
        self.min = thresholdMin
        self.max = thresholdMax
