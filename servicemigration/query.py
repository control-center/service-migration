import copy


default = {
    "Data": "",
    "Headers": { "Content-Type": ["application/json"]},
    "Method": "POST",
    "RequestURI": "",
}


def deserialize(data):
    """
    Parse data into a Query.
    """
    query = Query()
    if not data:
        return query
    query._Query__data = data
    query.data = data.get("Data")
    query.headers = data.get("Headers")
    query.method = data.get("Method")
    query.requestURI = data.get("RequestURI")
    return query


def serialize(query):
    """
    Dump a Query as data.
    """
    data = copy.deepcopy(query._Query__data)
    data["Data"] = query.data
    data["Headers"] = query.headers
    data["Method"] = query.method
    data["RequestURI"] = query.requestURI
    return data
    

class Query(object):
    """
    Wraps a single Query object.
    """
    def __init__(self, data=None, headers=None, method="", requestURI=""):
        self.__data = copy.deepcopy(default)
        self.data = data
        self.headers = headers or {}
        self.method = method or "POST"
        self.requestURI = requestURI
