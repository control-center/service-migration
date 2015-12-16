import copy

default = {
    "Name": "",
    "Script": ""
}

def deserialize(data):
    """
    Deserializes a list of Prereqs.
    """
    prereqs = []
    if data is None:
        return []
    for jsonPr in data:
        pr = Prereq()
        pr.name = jsonPr.get("Name", "")
        pr.script = jsonPr.get("Script", "")
        prereqs.append(pr)
    return prereqs

def serialize(prereqs):
    """
    Serializes a list of prereqs
    """
    data = []
    for pr in prereqs:
        data.append({"Name": pr.name, "Script": pr.script})
    return data


class Prereq(object):
    """
    Wraps a single service preeq
    """

    def __init__(self, name="", script=""):
        self.__data = copy.deepcopy(default)
        self.name = name
        self.script = script

