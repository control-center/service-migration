import copy

import endpoint
import volume
import healthcheck
import instancelimits
import configfile
import command

RESTART = -1
STOP = 0
RUN = 1
PAUSE = 2

def deserialize(data):
    """
    Deserializes a single service.
    """
    service = Service()
    service._Service__data = data
    service.name = data.get("Name", "")
    service.description = data.get("Description", "")
    service.startup = data.get("Startup", "")
    service.desiredState = data.get("DesiredState", STOP)
    service.endpoints = endpoint.deserialize(data.get("Endpoints", []))
    service.commands = command.deserialize(data.get("Commands", {}))
    service.volumes = volume.deserialize(data.get("Volumes", []))
    service.healthChecks = healthcheck.deserialize(data.get("HealthChecks", {}))
    service.instanceLimits = instancelimits.deserialize(data.get("InstanceLimits", {}))
    service.configFiles = configfile.deserialize(data.get("OriginalConfigs", {}))
    service.tags = data["Tags"][:] if data.get("Tags") is not None else []
    return service

def serialize(service):
    """
    Serializes a single service.
    """
    data = copy.deepcopy(service._Service__data)
    data["Name"] = service.name
    data["Description"] = service.description
    data["Startup"] = service.startup
    data["DesiredState"] = service.desiredState
    data["Endpoints"] = endpoint.serialize(service.endpoints)
    data["Commands"] = command.serialize(service.commands)
    data["Volumes"] = volume.serialize(service.volumes)
    data["HealthChecks"] = healthcheck.serialize(service.healthChecks)
    data["InstanceLimits"] = instancelimits.serialize(service.instanceLimits)
    data["OriginalConfigs"] = configfile.serialize(service.configFiles)
    data["Tags"] = service.tags[:]
    return data


class Service():
    """
    Wraps a single service.
    """

    def __init__(self, name="", description="", startup="",
        desiredState=STOP, endpoints=[], commands=[], volumes=[], 
        healthChecks=[], instanceLimits=None, configFiles=[],
        tags=[]):
        """
        Internal use only. Do not call to create a service.
        """
        self.__data = None
        self.name = name
        self.description = description
        self.startup = startup
        self.desiredState = desiredState
        self.endpoints = endpoints
        self.commands = commands
        self.volumes = volumes
        self.healthChecks = healthChecks
        self.instanceLimits = instancelimits.InstanceLimits() if instanceLimits is None else instanceLimits
        self.configFiles = configFiles
        self.tags = tags

    def clone(self):
        cl = copy.deepcopy(self)
        cl._Service__data["ID"] = "new-service"
        return cl

