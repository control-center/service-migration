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
    service.instances = data.get("Instances", 0)
    service.instanceLimits = instancelimits.deserialize(data.get("InstanceLimits", {}))
    service.originalConfigs = configfile.deserialize(data.get("OriginalConfigs", {}))
    service.oomKillDisable = data.get("OomKillDisable", False)
    service.oomScoreAdj = data.get("OomScoreAdj", 0)
    service.configFiles = configfile.deserialize(data.get("ConfigFiles", {}))
    service.monitoringProfile = monitoringprofile.deserialize(data.get("MonitoringProfile", {}))
    service.tags = data["Tags"][:] if data.get("Tags") is not None else []
    service.logConfigs = logconfig.deserialize(data.get("LogConfigs", []))
    service.prereqs = prereq.deserialize(data.get("Prereqs", []))
    service.ramCommitment = data.get("RAMCommitment", [])
    service.imageID = data.get("ImageID", "")
    service.emergencyShutdownLevel = data.get("EmergencyShutdownLevel", 0)
    service.startLevel = data.get("StartLevel", 0)
    service.changeOptions = data.get("ChangeOptions", [])
    service.hostPolicy = data.get("HostPolicy", "")
    service.privileged = data.get("Privileged", False)
    service.environment = data["Environment"][:] if data.get("Environment") is not None else []
    service.context = data["Context"].copy() if data.get("Context") is not None else {}
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
    data["Instances"] = service.instances
    data["InstanceLimits"] = instancelimits.serialize(service.instanceLimits)
    data["OriginalConfigs"] = configfile.serialize(service.originalConfigs)
    data["OomKillDisable"] = service.oomKillDisable
    data["OomScoreAdj"] = service.oomScoreAdj
    data["ConfigFiles"] = configfile.serialize(service.configFiles)
    data["MonitoringProfile"] = monitoringprofile.serialize(service.monitoringProfile)
    data["Tags"] = service.tags[:]
    data["LogConfigs"] = logconfig.serialize(service.logConfigs)
    data["Prereqs"] = prereq.serialize(service.prereqs)
    data["RAMCommitment"] = service.ramCommitment
    data["ImageID"] = service.imageID
    data["EmergencyShutdownLevel"] = service.emergencyShutdownLevel
    data["StartLevel"] = service.startLevel
    data["ChangeOptions"] = service.changeOptions
    data["HostPolicy"] = service.hostPolicy
    data["Privileged"] = service.privileged
    data["Environment"] = service.environment[:]
    data["Context"] = service.context.copy()
    return data


class Service(object):
    """
    Wraps a single service.
    """

    def __init__(self, name="", description="", startup="",
        desiredState=STOP, endpoints=None, commands=None, volumes=None,
        healthChecks=None, instanceLimits=None, originalConfigs=None,
        configFiles=None, monitoringProfile=None, tags=None, logConfigs=None,
        prereqs=None, ramCommitment=None, imageID = "", emergencyShutdownLevel=0,
        startLevel=0, instances=0, changeOptions=None, hostPolicy="",
        privileged=False, environment=None, context=None, oomKillDisable=False,
        oomScoreAdj=0):
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
        self.instances = 0
        self.instanceLimits = instancelimits.InstanceLimits() if instanceLimits is None else instanceLimits
        self.originalConfigs = originalConfigs or []
        self.oomKillDisable = oomKillDisable
        self.oomScoreAdj = oomScoreAdj
        self.configFiles = configFiles or []
        self.monitoringProfile = monitoringProfile
        self.tags = tags or []
        self.logConfigs = logConfigs or []
        self.prereqs = prereqs or []
        self.ramCommitment = ramCommitment or []
        self.imageID = imageID
        self.emergencyShutdownLevel = emergencyShutdownLevel
        self.startLevel = startLevel
        self.changeOptions = changeOptions
        self.hostPolicy = hostPolicy
        self.privileged = privileged
        self.environment = environment or []
        self.context = context or {}

    def clone(self):
        cl = copy.deepcopy(self)
        cl._Service__data["ID"] = "new-service"
        return cl

