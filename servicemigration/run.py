
def deserialize(data):
    """
    Deserializes a list of Runs.
    """
    if data is None:
        return []
    runs = []
    for k,v in data.iteritems():
        runs.append(Run(k, v))
    return runs

def serialize(runs):
    """
    Serializes a list of runs.
    """
    data = {}
    for run in runs:
        data[run.name] = run.command
    return data


class Run:
    """
    Wraps a single service run.
    """
    def __init__(self, name, command):
        self.name = name
        self.command = command


