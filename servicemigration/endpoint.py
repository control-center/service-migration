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
    "VHostList": [],
    "PortList": [],
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
        endpoint.name = ep.get("Name", "")
        endpoint.purpose = ep.get("Purpose", "")
        endpoint.application = ep.get("Application", "")
        endpoint.portnumber = ep.get("PortNumber", 0)
        endpoint.porttemplate = ep.get("PortTemplate", "")
        endpoint.protocol = ep.get("Protocol", "")
        endpoint.addressConfig = config.deserialize(ep.get("AddressConfig", {}))
        endpoint.applicationtemplate = ep.get("ApplicationTemplate", "")
        endpoint.vhostlist = ep.get("VHostList", [])
        endpoint.portlist = ep.get("PortList", [])
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
        d["PortTemplate"] = ep.porttemplate
        d["Protocol"] = ep.protocol
        d["AddressConfig"] = config.serialize(ep.addressConfig)
        d["ApplicationTemplate"] = ep.applicationtemplate
        d["VHostList"] = ep.vhostlist
        d["PortList"] = ep.portlist
        data.append(d)
    return data


class Endpoint(object):
    """
    Wraps a single service endpoint.
    """
    def __init__(self, name="", purpose="", application="", portnumber=0,
                 protocol="", addressConfig=None, applicationtemplate="",
                 porttemplate="", vhostlist=[], portlist=[]):
        self.__data = copy.deepcopy(default)
        self.name = name
        self.purpose = purpose
        self.application = application
        self.portnumber = portnumber
        self.porttemplate = porttemplate
        self.protocol = protocol
        self.addressConfig = config.AddressConfig() if addressConfig is None else addressConfig
        self.applicationtemplate = applicationtemplate
        self.vhostlist = vhostlist
        self.portlist = portlist
