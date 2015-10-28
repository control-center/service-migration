import copy


default = {
    "Name": "", 
    "Value": "",
}


def deserialize(data):
    """
    Deserializes a list of LogTags.
    """
    if not data:
        return []
    tags = []
    for datum in data:
        tag = LogTag()
        tag._LogTag__data = datum
        if datum.get("Name"):
            tag.name = datum["Name"]
        if datum.get("Value"):
            tag.value = datum["Value"]
        tags.append(tag)
    return tags


def serialize(tags):
    """
    Serializes a single LogTag.
    """
    data = []
    for tag in tags:
        datum = copy.deepcopy(tag._LogTag__data)
        datum.update({
            "Name": tag.name,
            "Value": tag.value,
        })
        data.append(datum)
    return data


class LogTag(object):
    """
    Wraps a single LogTag.
    """

    def __init__(self, name=None, value=None):
        self.__data = copy.deepcopy(default)
        self.name = name
        self.value = value
