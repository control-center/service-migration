import os
import re
import sys
import json
import copy

try:
    from Products.ZenUtils.controlplane.application import getConnectionSettings
    from Products.ZenUtils.controlplane import ControlPlaneClient, ServiceTree
    ZenUtils = True
except:
    ZenUtils = False

from version import versioned
import service
import exceptions

class ServiceContext(object):

    @versioned
    def __init__(self, filename=None):
        """
        Initializes the ServiceContext.

        Input precedence is:
            1. The filename argument passed to this function.
            2. The MIGRATE_INPUTFILE, which is an environment variable
               indicating the path to a json-formatted file containing
               the services to load.
            3. Acquisition of the services from serviced via the ZenUtils
               library.

        If 1 is not available, 2 will be used. If 1 & 2 are not available,
        3 will be used. If none are available, an error will be thrown.

        Requires that servicemigration.require() has been called.
        """
        infile = None
        if filename is not None:
            infile = filename
        else:
            infile = os.environ["MIGRATE_INPUTFILE"] if "MIGRATE_INPUTFILE" in os.environ else None

        self._client = ControlPlaneClient(**getConnectionSettings())

        if infile is not None:
            data = json.loads(open(infile, 'r').read())
        elif ZenUtils and "CONTROLPLANE_TENANT_ID" in os.environ:
            data = self._client.getServicesForMigration(os.environ["CONTROLPLANE_TENANT_ID"])
        else:
            raise exceptions.ServiceMigrationError("Can't find migration input data.")

        self.services = []
        self.__deploy = []
        if type(data) is dict:
            # Handle the case wherein we are reading from SDK output.
            for datum in data["Modified"]:
                self.services.append(service.deserialize(datum))
            for datum in data["Added"]:
                self.services.append(service.deserialize(datum))
            for datum in data["Deploy"]:
                self.__deploy.append(datum)
        elif type(data) is list:
            # Handle the case wherein we are reading from Serviced output.
            for datum in data:
                self.services.append(service.deserialize(datum))
        else:
            raise exceptions.ServiceMigrationError("Can't read migration input data.")
        if len(self.services) == 0:
            self.version = ""
        else:
            self.version = self.services[0]._Service__data["Version"]


    def commit(self, filename=None):
        """
        Commits the service to the given filename.

        Output precedence is:
            1. The filename argument passed to this function.
            2. The MIGRATE_OUTPUTFILE, which is an environment variable
               indicating the path to which to write a json-formatted file
               containing the services to commit.
            3. Posting of the services to serviced via the ZenUtils
               library.

        If 1 is not available, 2 will be used. If 1 & 2 are not available,
        3 will be used. If none are available, an error will be thrown.
        """
        addedServices = []
        modifiedServices = []
        for svc in self.services:
            serial = service.serialize(svc)
            serial["Version"] = self.version
            if serial["ID"] == "new-service":
                addedServices.append(serial)
            else:
                modifiedServices.append(serial)
        serviceId = self.getTopService()._Service__data["ID"]
        data = {
            "ServiceID": serviceId,
            "Modified": modifiedServices,
            "Added": addedServices,
            "Deploy": self.__deploy
        }
        data = json.dumps(data, indent=4, sort_keys=True)

        outfile = None
        if filename is not None:
            outfile = filename
        else:
            outfile = os.environ["MIGRATE_OUTPUTFILE"] if "MIGRATE_OUTPUTFILE" in os.environ else None
        if outfile is not None:
            f = open(outfile, 'w')
            f.write(data)
            f.close()
        elif ZenUtils:
            self._client.postServicesForMigration(data, serviceId)
        else:
            raise exceptions.ServiceMigrationError("Can't find migration output location.")

    def getServiceParent(self, svc):
        # This could be sped up by creating a map of ID:service, but let's not optimize prematurely.
        parents = filter(lambda s: s._Service__data["ID"] == svc._Service__data["ParentServiceID"], self.services)
        if len(parents) > 1:
            raise ValueError("A service cannot have more than one parent.")
        if len(parents) == 0:
            return None
        else:
            return parents[0]

    def getServiceChildren(self, svc):
        return filter(lambda s: s._Service__data["ParentServiceID"] == svc._Service__data["ID"], self.services)

    def getServicePath(self, svc):
        parent = self.getServiceParent(svc)
        if parent is None:
            return svc.name
        return self.getServicePath(parent) + "/" + svc.name

    def cycleCheckService(self, svc, history=None):
        if history is None:
            history = []
        if svc._Service__data["ID"] in history:
            raise ValueError("Cycle detected in service tree.")
        history.append(svc._Service__data["ID"])
        parent = self.getServiceParent(svc)
        if parent is None:
            return
        self.cycleCheckService(parent, history)

    def reparentService(self, svc, newParent):
        oldParent = self.getServiceParent(svc)
        if oldParent is None:
            raise ValueError("Can't reparent tenant.")
        if newParent._Service__data["ID"] == "new-service":
            raise ValueError("Can't reparent to a new service.")
        svc._Service__data["ParentServiceID"] = newParent._Service__data["ID"]
        # Check for cycles. If any are found, an error will be thrown.
        self.cycleCheckService(svc)

    def getTopService(self, svc=None):
        """
        Returns the service with no parents. There should be only one, and it
        should be the topmost in the portion of the service tree we have.
        """
        if svc is None:
            svc = self.services[0]
        parent = self.getServiceParent(svc)
        if parent is None:
            return svc
        return self.getTopService(parent)

    def findService(self, path):
        """
        Returns the service whose path exactly equal to the string path. If no
        such service exists, returns None.
        """
        matches = filter(lambda s: self.getServicePath(s) == path, self.services)
        return matches[0] if len(matches) == 1 else None

    def findServices(self, pattern):
        """
        Returns the list of services matching the regex pattern. Returns an empty list
        if no matches are found.
        """
        p = re.compile(pattern)
        return filter(lambda s: p.match(self.getServicePath(s)) != None, self.services)

    def deployService(self, servicedef, parent):
        """
        Add service definition for deployment.
        """
        if parent._Service__data["ID"] == "new-service":
            raise Exception("Can't deploy a service to a parent that is a new service.")
        self.__deploy.append({
            "Service": json.loads(servicedef),
            "ParentID": parent._Service__data["ID"]
        })

    def __deployService(self, service, parentid):
        """
        Add a service definition for deployment using parent ID. This is private
        because we don't want to expose service IDs, but need to use the parent
        ID when deploying from ZenPack.py.
        """
        svcs = filter(lambda s: s._Service__data["ID"] == parentid, self.services)
        if len(svcs) != 1:
            raise Exception("Couldn't find the proper parent service.")
        self.deployService(service, svcs[0])
