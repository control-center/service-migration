import copy

import addressconfig as config

default = {
    "Name": "",
    "Purpose": "",
    "Protocol": "",
    "PortNumber": 0,
    "PortTemplate": "",
    "VirtualAddress": "",
    "Application": "",
    "ApplicationTemplate": "",
    "AddressConfig": {
        "Port": 0,
        "Protocol": ""
    },
    "VHosts": None,
    "AddressAssignment": {
        "ID": "",
        "AssignmentType": "",
        "HostID": "",
        "PoolID": "",
        "IPAddr": "",
        "Port": 0,
        "ServiceID": "",
        "EndpointName": ""
    }
}

def deserialize(data):
    """
    Deserializes the list of endpoints.
    """
    if data is None:
        return []
    endpoints = []
    for ep in data:
        endpoint = Endpoint()
        endpoint._Endpoint__data = ep
        endpoint.name = ep["Name"]
        endpoint.purpose = ep["Purpose"]
        endpoint.application = ep["Application"]
        endpoint.portnumber = ep["PortNumber"]
        endpoint.protocol = ep["Protocol"]
        endpoint.addressConfig = config.deserialize(ep.get("AddressConfig", {}))
        endpoints.append(endpoint)
    return endpoints

def serialize(endpoints):
    """
    Serializes the list of endpoints.
    """
    data = []
    for ep in endpoints:
        d = {}
        d = copy.deepcopy(ep._Endpoint__data)
        d["Name"] = ep.name
        d["Purpose"] = ep.purpose
        d["Application"] = ep.application
        d["PortNumber"] = ep.portnumber
        d["Protocol"] = ep.protocol
        d["AddressConfig"] = config.serialize(ep.addressConfig)
        data.append(d)
    return data


class Endpoint(object):
    """
    Wraps a single service endpoint.
    """
    def __init__(self, name="", purpose="", application="", portnumber=0, protocol="", addressConfig=None):
        self.__data = copy.deepcopy(default)
        self.name = name
        self.purpose = purpose
        self.application = application
        self.portnumber = portnumber
        self.protocol = protocol
        self.addressConfig = config.AddressConfig() if addressConfig is None else addressConfig
