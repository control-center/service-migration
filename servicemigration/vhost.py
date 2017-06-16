import copy

default = {
    "Name": "",
    "Enabled": False
}

def deserialize(data):
    """
    Deserializes the list of VHosts
    :param data:
    :return: list of VHosts
    """
    if data is None:
        return []
    vhosts = []
    for vh in data:
        vhost = VHost()
        vhost._VHost__data = vh
        vhost.name = vh.get("Name", "")
        vhost.enabled = vh.get("Enabled", False)
        vhosts.append(vhost)
    return vhosts

def serialize(vhosts):
    """
    Serializes the list of vhosts
    :param vhosts:
    :return: a list of vhosts dicts
    """
    data = []
    for vh in vhosts:
        d = {}
        d = copy.deepcopy(vh._VHost__data)
        d["Name"] = vh.name
        d["Enabled"] = vh.enabled
        data.append(d)
    return data

class VHost(object):
    """
    Wraps a single VHost
    """
    def __init__(self, name="", enabled=False):
        self.__data = copy.deepcopy(default)
        self.name = name
        self.enabled = enabled
