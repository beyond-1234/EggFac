from enum import Enum

class TaskStatus(Enum):
    CREATED = 0
    STARTED = 1
    ENDED = 2
    ABORTED = 3
