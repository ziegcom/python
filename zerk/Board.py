from Position import Position
import Util

import sys
import random
from random import shuffle

################################################################################
# Version compatibility BS
################################################################################

try:
    from termcolor import colored
except ImportError:
    def colored(c, shade):
        return c

################################################################################
# Represent an N x N playing board with obstacles, monsters, items and a player.
################################################################################
class Board:

    def __init__(self, size):
        self.size = size
        self.obstacles = set()  # set of Positions
        self.monsters = []      # list of mobile monsters on the board
        self.items = []         # list of items on the board
        self.player = None
        self.trail = set()      # set of Positions (breadcrumbs)

    ############################################################################
    #                                                                          #
    #                             Initialization                               #
    #                                                                          #
    ############################################################################

    def createObstacles(self, count, size):
        # iterate over each obstacle we're to emplace
        for i in range(0, count):

            # pick an unoccupied starting point for the boulder
            pos = self.randomUnoccupiedPos()
            self.obstacles.add(pos)

            # flesh-out the obstacle in all its ugly wartiness
            for j in range(1, size - 1):
                pos = self.randomAdjacentUnoccupiedPos(pos)
                if pos is None:
                    break
                self.obstacles.add(pos)

    def addMonster(self, m):
        m.pos = self.randomUnoccupiedPos()
        self.monsters.append(m)

    def addItem(self, item):
        item.pos = self.randomUnoccupiedPos()
        self.items.append(item)

    def addPlayer(self, player):
        player.pos = self.randomUnoccupiedPos()
        self.player = player

    ############################################################################
    #                                                                          #
    #                              Accessors                                   #
    #                                                                          #
    ############################################################################

    def getMonsters(self):
        return self.monsters

    def getItems(self, pos):
        for item in self.items:
            if item.pos == pos:
                yield item

    def removeItem(self, item):
        if item in self.items:
            self.items.remove(item)

    def updatePositions(self):
        # update our trail of breadcrumbs
        self.trail.add(self.player.pos)

        # wandering monsters wander
        for m in self.monsters:

            if not m.alive:
                continue;

            origPos = m.pos

            # how many spaces this monster can move per turn
            for move in range(0, m.speed):

                # the more aggressive a monster is, the more it will try to move toward the player
                dist = m.pos.dist(self.player.pos)

                # consider up to 'aggression' possible moves from this spot,
                # looking for one that will move toward the hapless player
                for check in range (m.aggression + 1):
                    newPos = self.randomAdjacentUnoccupiedPos(m.pos)
                    if newPos is not None:
                        if (newPos.dist(self.player.pos) < dist) or (check >= m.aggression):
                            m.pos = newPos
                            break

            # increase entropy when Baby is stuck in a corner
            if origPos == m.pos:
                m.aggression = max(0, m.aggression - 1)
            else:
                m.aggression = min(m.origAggression, m.aggression + 1)

    ############################################################################
    #                                                                          #
    #                          Position Helpers                                #
    #                                                                          #
    ############################################################################

    def occupied(self, pos):
        # check to see that no obstacles occupy this position
        for obstaclePos in self.obstacles:
            if obstaclePos == pos:
                return True

        # do NOT check for items or monsters!
        return False

    def randomUnoccupiedPos(self):
        pos = self.randomPos()
        while self.occupied(pos):
            pos = self.randomPos()
        return pos

    def randomAdjacentUnoccupiedPos(self, pos):
        directions = ["n", "e", "s", "w"]
        shuffle(directions)
        for direction in directions:
            if (self.canMove(pos, direction)):
                p2 = self.adjacentPos(pos, direction)
                if not self.occupied(p2):
                    return p2
        return None

    def listAvailableDirections(self, pos):
        avail = []
        directions = ["n", "e", "s", "w"]
        for direction in directions:
            if (self.canMove(pos, direction)):
                avail.append(self.expandDirection(direction))
        return Util.prettyList(avail, "or")

    def expandDirection(self, direction):
        if direction == "e":
            return "east"
        elif direction == "w":
            return "west"
        elif direction == "n":
            return "north"
        elif direction == "s":
            return "south"
        raise Exception("unknown direction: %s" % direction)

    def randomPos(self):
        return Position(random.randint(0, self.size - 1),
                        random.randint(0, self.size - 1))

    def canMove(self, pos, direction):
        if pos is None:
            return False

        if direction == "n":
            return pos.y > 0
        elif direction == "s":
            return pos.y < self.size - 1
        elif direction == "w":
            return pos.x > 0
        elif direction == "e":
            return pos.x < self.size - 1
        raise Exception("unknown direction: %s" % direction)

    def adjacentPos(self, pos, direction):
        if not self.canMove(pos, direction):
            raise Exception("can't move %s from %s" % (direction, pos))

        if direction == "n":
            return Position(pos.x, pos.y - 1)
        elif direction == "s":
            return Position(pos.x, pos.y + 1)
        elif direction == "w":
            return Position(pos.x - 1, pos.y)
        elif direction == "e":
            return Position(pos.x + 1, pos.y)
        raise Exception("unknown direction: %s" % direction)

    ############################################################################
    #                                                                          #
    #                               Display                                    #
    #                                                                          #
    ############################################################################

    def showTrail(self):
        self.dump(label="Breadcrumbs")

    def dump(self, **kwargs):
        # label
        if 'label' in kwargs:
            print("%s:" % kwargs['label'])

        # map
        for y in range(0, self.size):
            for x in range(0, self.size):
                sys.stdout.write(self.getDisplayChar(Position(x, y), **kwargs) + ' ')
            sys.stdout.write('\n')

        # key
        if not 'admin' in kwargs:
            sys.stdout.write("Key: #=boulder @=player ^=north\n")
        else:
            sys.stdout.write("Key: #=boulder @=player ^=north &=monster *=item\n")
            for m in self.monsters:
                print("%s at %s (aggression %d)" % (m.name, m.pos, m.aggression))
            for i in self.items:
                print("%s at %s" % (i.name, i.pos))
        print("")

    def getDisplayChar(self, pos, **kwargs):
        if pos in self.obstacles:
            return '#'

        # require God-mode to see monsters and items
        if 'admin' in kwargs:
            for m in self.monsters:
                if pos == m.pos:
                    return colored(m.char if hasattr(m, 'char') else '&', 'red')

            for i in self.items:
                if pos == i.pos:
                    return colored(i.char if hasattr(i, 'char') else '*', 'yellow')

        if self.player is not None:
            if pos == self.player.pos:
                return colored(self.player.char if hasattr(self.player, 'char') else '@', 'cyan')

        if pos in self.trail:
            return colored('o', 'blue')

        return colored('.', 'green')
