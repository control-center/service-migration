
import sys
import json

from version import versioned

class Service():

    def __init__(self, data):
        self.__data = data

    @property
    def description(self):
        return self.__data["Description"]

    @description.setter
    def description(self, value):
        self.__data["Description"] = value



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
            serviceList.append(service._Service__data)
        f = open(filename, 'w')
        f.write(json.dumps(serviceList, indent=4, sort_keys=True))
        f.close()


