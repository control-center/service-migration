import re
import sys
import json

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
        for data in  json.loads(open(filename, 'r').read()):
            self.services.append(service.deserialize(data))
        if len(self.services) == 0:
            self.version = ""
        else:
            self.version = self.services[0]._Service__data["Version"]
        for svc in self.services:
            parent = filter(lambda s: s._Service__data["ID"] == svc._Service__data["ParentServiceID"], self.services)
            if len(parent) == 0:
                svc.parent = None
            else:
                svc.parent = parent[0]
                svc.parent.children.append(svc)

    def commit(self, filename=None):
        """
        Commits the service to the given filename. If filename is None,
        writes to the file defined by sys.argv[2].
        """
        if filename is None:
            filename = sys.argv[2]
        serviceList = []
        for svc in self.services:
            serviceList.append(service.serialize(svc))
        for svc in serviceList:
            svc["Version"] = self.version
        f = open(filename, 'w')
        f.write(json.dumps(serviceList, indent=4, sort_keys=True))
        f.close()

    def findService(self, path):
        """
        Returns the service whose path exactly equal to the string path. If no
        such service exists, returns None.
        """
        matches = filter(lambda s: s.getPath() == path, self.services)
        return matches[0] if len(matches) == 1 else None

    def findServices(self, pattern):
        """
        Returns the list of services matching the regex pattern. Returns an empty list
        if no matches are found.
        """
        p = re.compile(pattern)
        return filter(lambda s: p.match(s.getPath()) != None, self.services)


