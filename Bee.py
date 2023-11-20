from enum import Enum

class BeeStatus(Enum):
    RESTING = 0
    BORED = 1
    DANCING = 2
    SEARCHING = 3
    FLYING_TO_FLOWER = 4
    RETURNING_TO_HIVE = 5

class Bee:

    def __init__(self, id):
        self.id = id
        self.destination = (0, 0)
        self.memory = []
        self.status = BeeStatus.BORED


