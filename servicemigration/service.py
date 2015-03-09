import sys
import json
import copy

from version import versioned


class Service():

    def __init__(self, data):
        self.__data = data
        self.description = data["Description"]
        self.runs = copy.copy(data["Runs"])

    def __toObject(self):
        newObj = copy.deepcopy(self.__data)
        newObj["Description"] = self.description
        newObj["Runs"] = self.runs
        return newObj

class ServiceContext():

    @versioned
    def __init__(self, filename=None):
        if filename is None:
            filename = sys.argv[1]
        self.services = []
        for data in  json.loads(open(filename, 'r').read()):
            self.services.append(Service(data))

    def commit(self, filename=None):
        if filename is None:
            filename = sys.argv[2]
        serviceList = []
        for service in self.services:
            serviceList.append(service._Service__toObject())
        f = open(filename, 'w')
        f.write(json.dumps(serviceList, indent=4, sort_keys=True))
        f.close()


