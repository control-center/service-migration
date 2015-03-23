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


