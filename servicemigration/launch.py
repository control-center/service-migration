from enum import Enum

def deserialize(data):
    """
    Deserializes a "Launch" enumeration.
    """
    return Launch[data]
    
def serialize(launch):
    """
    Serializes a "Launch" enumerations.
    """
    return launch.name


class Launch(Enum):
    """
    Wraps a "Launch" enumeration.
    """
    auto = 1
    manual = 2

# Default enumeration value
default = Launch.auto

