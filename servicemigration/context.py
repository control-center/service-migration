import re
import sys
import json
import copy

from version import versioned
import service

class ServiceContext():

    @versioned
    def __init__(self, filename=None):
        """
        Initializes the ServiceContext for the given filename, or the file
        defined by sys.argv[1] if filename is None.

        Requires that servicemigration.require() has been called.
        """
        if filename is None:
            filename = sys.argv[1]
        self.services = []
        data = json.loads(open(filename, 'r').read())
        if type(data) is dict:
            # Handle the case wherein we're loading the test results.
            for datum in data["modified"]:
                self.services.append(service.deserialize(datum))
            for datum in data["cloned"]:
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
        Commits the service to the given filename. If filename is None,
        writes to the file defined by sys.argv[2].
        """
        if filename is None:
            filename = sys.argv[2]
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
            "modified": serviceList,
            "cloned": cloneList
        }
        f = open(filename, 'w')
        f.write(json.dumps(data, indent=4, sort_keys=True))
        f.close()

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

