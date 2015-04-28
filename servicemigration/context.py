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

class ServiceContext():

    @versioned
    def __init__(self, filename=None):
        """
        Initializes the ServiceContext. Input precedence is filename,
        MIGRATE_INPUTFILE, servicemigration endpoint.

        Requires that servicemigration.require() has been called.
        """
        cpClient = None
        if ZenUtils:
            cpClient = ControlPlaneClient(**getConnectionSettings())
        data = None
        if filename is not None:
            data = json.loads(open(filename, 'r').read())
        else:
            infile = os.environ["MIGRATE_INPUTFILE"] if "MIGRATE_INPUTFILE" in os.environ else None
            if infile is not None:
                data = json.loads(open(infile, 'r').read())
            elif ZenUtils and "CONTROLPLANE_TENANT_ID" in os.environ:
                data = cpClient.getServicesForMigration(os.environ["CONTROLPLANE_TENANT_ID"])
            else:
                raise ValueError("Can't find migration input data.")

        self.services = []
        if type(data) is dict:
            # Handle the case wherein we're loading the test results.
            for datum in data["Modified"]:
                self.services.append(service.deserialize(datum))
            for datum in data["Cloned"]:
                self.services.append(service.deserialize(datum))
        else:
            # Handle the case wherein we're loading input from serviced.
            for datum in data:
                self.services.append(service.deserialize(datum))
        if len(self.services) == 0:
            self.version = ""
        else:
            self.version = self.services[0]._Service__data["Version"]

    def commit(self, filename=None):
        """
        Commits the service to the given filename. Output precedence
        is filename, MIGRATE_OUTPUTFILE, servicemigration endpoint.
        """
        serviceList = []
        cloneList = []
        for svc in self.services:
            serial = service.serialize(svc)
            serial["Version"] = self.version
            if svc._Service__clone:
                cloneList.append(serial)
            else:
                serviceList.append(serial)
        data = {
            "ServiceID": self.getTopService()._Service__data["ID"],
            "Modified": serviceList,
            "Cloned": cloneList
        }
        data = json.dumps(data, indent=4, sort_keys=True)
        cpClient = None
        if ZenUtils:
            cpClient = ControlPlaneClient(**getConnectionSettings())
        if filename is not None:
            f = open(filename, 'w')
            f.write(data)
            f.close()
        else:
            outfile = os.environ["MIGRATE_OUTPUTFILE"] if "MIGRATE_OUTPUTFILE" in os.environ else None
            if outfile is not None:
                f = open(outfile, 'w')
                f.write(data)
                f.close()
            elif ZenUtils:
                cpClient.postServicesForMigration(data)
            else:
                raise ValueError("Can't find migration input data.")

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
        if newParent._Service__clone is True:
            raise ValueError("Can't reparent to a clone.")
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

    def cloneService(self, svc):
        """
        Returns a clone of the provided service. The clone is added to the context service list.
        """
        if self.getServiceParent(svc) is None:
            raise ValueError("Can't clone tenant.")
        clone = copy.deepcopy(svc)
        clone._Service__clone = True
        self.services.append(clone)
        return clone

