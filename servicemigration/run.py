
def deserialize(data):
    if data is None:
        return []
    runs = []
    for k,v in data.iteritems():
        runs.append(Run(k, v))
    return runs

def serialize(runs):
    data = {}
    for run in runs:
        data[run.name] = run.command
    return data


class Run:

    def __init__(self, name, command):
        self.name = name
        self.command = command


