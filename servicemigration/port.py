import copy

default = {
    "PortAddr": "",
    "Protocol": "",
    "Enabled": False,
    "UseTLS": False
}

def deserialize(data):
    """
    Deserializes the list of Ports
    :param data:
    :return: a list of Port instances
    """
    ports = []
    for p in data:
        port = Port()
        port._Port__data = p
        port.portaddr = p.get("PortAddr", "")
        port.protocol = p.get("Protocol", "")
        port.enabled = p.get("Enabled", False)
        port.usetls = p.get("UseTLS", False)
        ports.append(port)
    return ports

def serialize(ports):
    """
    Serializes the list of Ports
    :param ports:
    :return: a list of ports dicts
    """
    data = []
    for p in ports:
        d = {}
        d = copy.deepcopy(p._Port__data)
        d["PortAddr"] = p.portaddr
        d["Protocol"] = p.protocol
        d["Enabled"] = p.enabled
        d["UseTLS"] = p.usetls
        data.append(d)
    return data

class Port(object):
    """
    Wraps a sing Port
    """
    def __init__(self, portaddr="", protocol="", enabled=False, usetls=False):
        self.__data = copy.deepcopy(default)
        self.portaddr = portaddr
        self.protocol = protocol
        self.enabled = enabled
        self.usetls = usetls
