import copy

default = {
    "Owner": "",
    "Permission": "",
    "ResourcePath": "",
    "ContainerPath": "",
    "Type": ""
}

def deserialize(data):
    if data is None:
        return []
    volumes = []
    for volume in data:
        v = Volume()
        v._Volume__data = volume
        v.owner = volume["Owner"]
        v.permission = volume["Permission"]
        v.resourcePath = volume["ResourcePath"]
        v.containerPath = volume["ContainerPath"]
        volumes.append(v)
    return volumes

def serialize(volumes):
    data = []
    for volume in volumes:
        v = volume._Volume__data
        v["Owner"] = volume.owner
        v["Permission"] = volume.permission
        v["ResourcePath"] = volume.resourcePath
        v["ContainerPath"] = volume.containerPath
        data.append(v)
    return data

class Volume:

    def __init__(self, owner="", permission="", resourcePath="", containerPath=""):
        self.__data = copy.deepcopy(default)
        self.owner = owner
        self.permission = permission
        self.resourcePath = resourcePath
        self.containerPath = containerPath

