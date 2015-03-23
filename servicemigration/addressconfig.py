import copy

default = {
    "Port": 0,
    "Protocol": ""
}

def deserialize(data):
    """
    Deserializes a single AddressConfig.
    """
    config = AddressConfig()
    config._AddressConfig__data = data
    config.port = data["Port"]
    config.protocol = data["Protocol"]
    return config

def serialize(config):
    """
    Serializes a single AddressConfig.
    """
    data = copy.deepcopy(config._AddressConfig__data)
    data["Port"] = config.port
    data["Protocol"] = config.protocol
    return data


class AddressConfig:
    """
    Wraps a single AddressCconfig.
    """
    def __init__(self, port=0, protocol=""):
        self.__data = copy.deepcopy(default)
        self.port = port
        self.protocol = protocol

    def clear():
        self.__data = copy.deepcopy(default)