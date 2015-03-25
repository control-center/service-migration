import copy

import endpoint
import run
import volume
import healthcheck

def deserialize(data):
    """
    Deserializes a single service.
    """
    service = Service()
    service._Service__data = data
    service.name = data["Name"]
    service.description = data["Description"]
    service.startup = data["Startup"]
    service.endpoints = endpoint.deserialize(data["Endpoints"])
    service.runs = run.deserialize(data["Runs"])
    service.volumes = volume.deserialize(data["Volumes"])
    service.healthChecks = healthcheck.deserialize(data["HealthChecks"])
    return service

def serialize(service):
    """
    Serializes a single service.
    """
    data = copy.deepcopy(service._Service__data)
    data["Name"] = service.name
    data["Description"] = service.description
    data["Startup"] = service.startup
    data["Endpoints"] = endpoint.serialize(service.endpoints)
    data["Runs"] = run.serialize(service.runs)
    data["Volumes"] = volume.serialize(service.volumes)
    data["HealthChecks"] = healthcheck.serialize(service.healthChecks)
    return data


class Service():
    """
    Wraps a single service.
    """

    def __init__(self, name="", description="", startup="", endpoints=[], runs=[], volumes=[], healthChecks=[]):
        """
        Internal use only. Do not call to create a service.
        """
        self.parent = None
        self.children = []
        self.__path = None
        self.__data = None
        self.name = name
        self.description = description
        self.startup = startup
        self.endpoints = endpoints,
        self.runs = runs,
        self.volumes = volumes,
        self.healthChecks = healthChecks

    def getPath(self):
        """
        Returns the path through the service tree to this service.
        """
        if self.__path is not None:
            return self.__path
        if self.parent is None:
            return self.name
        self.__path = self.parent.getPath() + "/" + self.name
        return self.__path

