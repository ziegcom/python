import math

class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return self.x << 8 | self.y

    def dist(self, pos):
        return math.sqrt((self.x - pos.x) * (self.x - pos.x) +
                         (self.y - pos.y) * (self.y - pos.y))
