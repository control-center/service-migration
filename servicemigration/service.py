import copy

import endpoint
import run
import volume
import healthcheck
import instancelimits
import configfile

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
    service.name = data["Name"]
    service.description = data["Description"]
    service.startup = data["Startup"]
    service.desiredState = data["DesiredState"]
    service.endpoints = endpoint.deserialize(data["Endpoints"])
    service.runs = run.deserialize(data["Runs"])
    service.volumes = volume.deserialize(data["Volumes"])
    service.healthChecks = healthcheck.deserialize(data["HealthChecks"])
    service.instanceLimits = instancelimits.deserialize(data["InstanceLimits"])
    service.configFiles = configfile.deserialize(data["OriginalConfigs"])
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
    data["Runs"] = run.serialize(service.runs)
    data["Volumes"] = volume.serialize(service.volumes)
    data["HealthChecks"] = healthcheck.serialize(service.healthChecks)
    data["InstanceLimits"] = instancelimits.serialize(service.instanceLimits)
    data["OriginalConfigs"] = configfile.serialize(service.configFiles)
    return data


class Service():
    """
    Wraps a single service.
    """

    def __init__(self, name="", description="", startup="",
        desiredState=STOP, endpoints=[], runs=[], volumes=[], 
        healthChecks=[], instanceLimits=None, configFiles=[]):
        """
        Internal use only. Do not call to create a service.
        """
        self.__data = None
        self.__clone = False
        self.name = name
        self.description = description
        self.startup = startup
        self.desiredState = desiredState
        self.endpoints = endpoints
        self.runs = runs
        self.volumes = volumes
        self.healthChecks = healthChecks
        self.instanceLimits = instancelimits.InstanceLimits() if instanceLimits is None else instanceLimits
        self.configFiles = configFiles
