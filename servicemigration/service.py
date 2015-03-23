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
    def __init__(self, description="", startup="", endpoints=[], runs=[], volumes=[], healthChecks=[]):
        self.__data = None
        self.description = description
        self.startup = startup
        self.endpoints = endpoints,
        self.runs = runs,
        self.volumes = volumes,
        self.healthChecks = healthChecks

