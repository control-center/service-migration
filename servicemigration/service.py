import copy

import endpoint
import volume
import healthcheck
import instancelimits
import configfile
import command
import logconfig
import monitoringprofile
import prereq

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
    service.originalConfigs = configfile.deserialize(data.get("OriginalConfigs", {}))
    service.configFiles = configfile.deserialize(data.get("ConfigFiles", {}))
    service.monitoringProfile = monitoringprofile.deserialize(data.get("MonitoringProfile", {}))
    service.tags = data["Tags"][:] if data.get("Tags") is not None else []
    service.logConfigs = logconfig.deserialize(data.get("LogConfigs", []))
    service.prereqs = prereq.deserialize(data.get("Prereqs", []))
    service.ramCommitment = data.get("RAMCommitment", [])
    service.imageID = data.get("ImageID", "")
    service.version = data.get("Version", "")
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
    data["OriginalConfigs"] = configfile.serialize(service.originalConfigs)
    data["ConfigFiles"] = configfile.serialize(service.configFiles)
    data["MonitoringProfile"] = monitoringprofile.serialize(service.monitoringProfile)
    data["Tags"] = service.tags[:]
    data["LogConfigs"] = logconfig.serialize(service.logConfigs)
    data["Prereqs"] = prereq.serialize(service.prereqs)
    data["RAMCommitment"] = service.ramCommitment
    data["ImageID"] = service.imageID
    data["Version"] = service.version
    return data


class Service(object):
    """
    Wraps a single service.
    """

    def __init__(self, name="", description="", startup="",
        desiredState=STOP, endpoints=None, commands=None, volumes=None,
        healthChecks=None, instanceLimits=None, originalConfigs=None, 
        configFiles=None, monitoringProfile=None, tags=None, logConfigs=None, 
        prereqs=None, ramCommitment=None, imageID = "", version=""):
        """
        Internal use only. Do not call to create a service.
        """
        self.__data = None
        self.name = name
        self.description = description
        self.startup = startup
        self.desiredState = desiredState
        self.endpoints = endpoints or []
        self.commands = commands or []
        self.volumes = volumes or []
        self.healthChecks = healthChecks or []
        self.instanceLimits = instancelimits.InstanceLimits() if instanceLimits is None else instanceLimits
        self.originalConfigs = originalConfigs or []
        self.configFiles = configFiles or []
        self.monitoringProfile = monitoringProfile
        self.tags = tags or []
        self.logConfigs = logConfigs or []
        self.prereqs = prereqs or []
        self.ramCommitment = ramCommitment or []
        self.imageID = imageID
        self.version = version

    def clone(self):
        cl = copy.deepcopy(self)
        cl._Service__data["ID"] = "new-service"
        return cl

