import copy


default = {
    "Name": "", 
    "Enabled": "",
}


def deserialize(data):
    """
    Deserializes a list of vHosts.
    """
    if not data:
        return []
    vHosts = []
    for datum in data:
        vHost = VHost()
        vHost._VHost__data = datum
        if datum.get("Name"):
            vHost.name = datum["Name"]
        if datum.get("Enabled"):
            vHost.enabled = datum["Enabled"]
        vHosts.append(vHost)
    return vHosts


def serialize(vHosts):
    """
    Serializes a list of vHosts.
    """
    data = []
    for vHost in vHosts:
        datum = copy.deepcopy(vHost._VHost__data)
        datum.update({
            "Name": vHost.name,
            "Enabled": vHost.enabled,
        })
        data.append(datum)
    return data


class VHost(object):
    """
    Wraps a single vHost.
    """

    def __init__(self, name=None, enabled=False):
        self.__data = copy.deepcopy(default)
        self.name = name
        self.enabled = enabled
