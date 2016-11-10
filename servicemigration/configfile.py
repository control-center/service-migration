import copy

default = {
    "Filename": "/tmp/zenoss_config_file",
    "Owner": "zenoss:zenoss",
    "Permissions": "660",
    "Content": "# Zenoss config file"
}

def deserialize(data):
    """
    Deserializes a dict of ConfigFiles.
    """
    configfiles = []
    if data is None:
        return []
    for k, v in data.iteritems():
        cf = ConfigFile()
        cf._ConfigFile__data = v
        cf.name = k
        cf.filename = v.get("Filename", "")
        cf.owner = v.get("Owner", "")
        cf.permissions = v.get("Permissions", "")
        cf.content = v.get("Content", "")
        configfiles.append(cf)
    return configfiles

def serialize(configfiles):
    """
    Serializes a list of ConfigFiles.
    """
    data = {}
    for cf in configfiles:
        data[cf.name] = cf._ConfigFile__data
        data[cf.name]["Filename"] = cf.filename
        data[cf.name]["Owner"] = cf.owner
        data[cf.name]["Permissions"] = cf.permissions
        data[cf.name]["Content"] = cf.content
    return data


class ConfigFile(object):
    """
    Wraps a single service config file.
    """

    def __init__(self, name="", filename="", owner="", permissions="660", content=""):
        self.__data = copy.deepcopy(default)
        self.name = name
        self.filename = filename
        self.owner = owner
        self.permissions = permissions
        self.content = content
