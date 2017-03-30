from Position import Position

import sys
import random
from random import shuffle

class Board:
    """
    An N x N square matrix
    """

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

            # how many spaces this monster can move per turn
            moves = m.speed 

            for move in range(0, moves):
                
                # the more aggressive a monster is, the more it will try to move toward the player
                maxChecks = m.aggression
                dist = m.pos.dist(self.player.pos)

                # consider up to 'aggression' possible moves from this spot, 
                # looking for one that will move toward the hapless player
                for check in range (0, maxChecks):
                    newPos = self.randomAdjacentUnoccupiedPos(m.pos)
                    if newPos is not None:
                        if (newPos.dist(self.player.pos) < dist) or (check == maxChecks):
                            m.pos = newPos
                            break

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
        directions = ["n", "s", "e", "w"]
        shuffle(directions)
        for direction in directions:
            if (self.canMove(pos, direction)):
                p2 = self.adjacentPos(pos, direction)
                if not self.occupied(p2):
                    return p2
        # just return null
        # raise Exception("there are no adjacent unoccupied positions from %s" % pos)

    def randomPos(self):
        return Position(random.randint(0, self.size), 
                        random.randint(0, self.size))

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
        if 'label' in kwargs:
            print "%s:" % kwargs['label']

        for y in range(0, self.size):
            for x in range(0, self.size):
                sys.stdout.write(self.getDisplayChar(Position(x, y), **kwargs) + ' ')
            sys.stdout.write('\n')

    def getDisplayChar(self, pos, **kwargs):
        if pos in self.obstacles:
            return '#'
        
        # require God-mode to see monsters and items
        if 'admin' in kwargs:
            for m in self.monsters:
                if pos == m.pos:
                    return m.char if hasattr(m, 'char') else '&'

            for i in self.items:
                if pos == i.pos:
                    return i.char if hasattr(i, 'char') else '*'
                
        if self.player is not None:
            if pos == self.player.pos:
                return self.player.char if hasattr(self.player, 'char') else '@'

        if pos in self.trail:
            return 'o'

        return '.'
