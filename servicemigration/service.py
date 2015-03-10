import sys
import json

from version import versioned


class Service():

    def __init__(self, data):
        self.__data = data

    def getDescription(self):
        """
        Returns the service description string.
        """
        return self.__data["Description"]

    def setDescription(self, desc):
        """
        Set the service description string.
        """
        self.__data["Description"] = desc

    def getRuns(self):
        """
        Returns a map of string:string defining the service runs.
        """
        return {} if "Runs" not in self.__data else self.__data["Runs"]

    def setRuns(self, runs):
        """
        Sets the service runs value. Takes a map of string:string.
        """
        self.__data["Runs"] = runs


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
            self.services.append(Service(data))

    def commit(self, filename=None):
        """
        Commits the service to the given filename. If filename is None,
        writes to the file defined by sys.argv[2].
        """
        if filename is None:
            filename = sys.argv[2]
        serviceList = []
        for service in self.services:
            serviceList.append(service._Service__data)
        f = open(filename, 'w')
        f.write(json.dumps(serviceList, indent=4, sort_keys=True))
        f.close()


