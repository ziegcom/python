import Board
import Player
import Monster

import re
import random

################################################################################
#                                                                              #
#                          Compatibility Kludges                               #
#                                                                              #
################################################################################

# in 2.x, map raw_input() to 3.x's newer input()
try: 
    input = raw_input
except NameError: 
    pass

################################################################################
class Engine:

    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.gameOver = False
        self.confusion = 0

    def start(self):
        self.doWelcome()
        self.doLook()

        while not self.gameOver:
            self.board.updatePositions()
            self.proximityCheck()

            if not self.gameOver:
                cmd = input("What would you like to do? ")
                self.processCommand(cmd.lower())

    def processCommand(self, cmd):

        # inventory (do this first, before parsing off leading "I")
        if re.search("inventory", cmd) or cmd == "i":
            return self.doInventory()

        # peel-off implicit subject
        cmd = re.sub(r"^i\s+(.*)\s*$", r"\1", cmd)

        # help
        if re.search("help", cmd):
            return self.doHelp()

        # look
        if re.search('look', cmd):
            return self.doLook()

        # movement
        result = re.match(r'((go|walk|run|move)\s+)?(n(orth)?|e(ast)?|w(est)?|s(outh)?)\b', cmd)
        if result:
            direction = result.group(3)[0]
            return self.doMove(direction)

        # take
        result = re.match(r"(take|get|grab|steal|filch|acquire|obtain|pick.*up)\s+(the|an?)?\s*(\S+)", cmd)
        if result:
            itemName = result.group(3)
            return self.doTake(itemName)

        # map
        if re.search("map", cmd):
            return self.doMap()

        # wait
        if re.search(r"wait|sleep|pause|delay|nap", cmd):
            return self.doSleep()

        # debug
        if re.search("debug", cmd) and __debug__:
            return self.doDebug()

        # quit
        if re.search(r"quit|stop|end|exit|kill (me|self|myself)|shuffle off this mortal coil|self.*defenestrate", cmd):
            return self.endGame("You're a complete wuss. A waste of space. I've pushed out farts with more conviction than you.")

        # todo: drop/discard, attack/kill/slay, open, use, ...

        # otherwise
        print("I don't know how to %s.\n" % cmd)

        self.confusion += 1
        if self.confusion > 2:
            self.doHelp()
            self.confusion = 0

    def proximityCheck(self):
        for monster in self.board.getMonsters():
            if monster.alive:
                # did the monster just get us?
                if monster.pos == self.player.pos:
                    print(monster.loseMsg)
                    return self.endGame("You have died.")

                # emit spookiness
                dist = self.player.pos.dist(monster.pos)
                if dist <= 1.5:
                    print(monster.nearMsg)
                elif dist < 2.5:
                    print(monster.medMsg)
                elif dist < 3.5:
                    print(monster.farMsg)

    def endGame(self, msg):
        # add points for anything in their inventory
        for item in self.player.inventory:
            self.player.score += item.scoreValue

        print('\n' + msg)
        print("You have a score of %d points." % self.player.score)
        self.gameOver = True

    ############################################################################
    #                                                                          #
    #                             Command Library                              #
    #                                                                          #
    ############################################################################

    def doWelcome(self):
        print("Welcome to Zerk, the command-line adventure game of your dreams!\n")

    def doLook(self):
        print("You are in a vast underground cavern, whose broken landscape is fractured "
              "by scattered impassable piles of riven rock and rubble.  There is no single "
              "light source, but a vague dimness emanates from the rotting and pestilant "
              "fungus that fibrously clings to the moldering stone.\n"
              "\n"
              "From the slowly-cooling pile of damp excreta in which you just stepped, "
              "you take it that you are not alone in this inpenetrable and sound-devouring "
              "darkness.\n")
        print("You can go %s.\n" % self.board.listAvailableDirections(self.player.pos))

    def doMove(self, direction):
        pos = self.player.pos
        longDir = self.board.expandDirection(direction)

        if not self.board.canMove(pos, direction):
            print("The cavern wall prevents you from moving %s." % longDir)
            return

        p2 = self.board.adjacentPos(pos, direction)
        if self.board.occupied(p2):
            print("You cannot move %s due to a towering mass of unscalable rubble." % longDir)
            return

        print("You travel %s." % longDir)
        self.player.pos = p2

        # any monsters here?
        for monster in self.board.getMonsters():
            if monster.pos == self.player.pos:
                # until we implement combat logic, follow chess rules: if we move into
                # the monster's space, we win
                if monster.alive:
                    print(monster.winMsg)
                    self.player.score += monster.scoreValue
                    monster.alive = False
                else:
                    print(monster.corpseMsg)

        # any items here?
        for item in self.board.getItems(self.player.pos):
            print(item.lookMsg)

    def doTake(self, itemName):
        found = False

        # pick up any items at this location matching the given name
        for item in self.board.getItems(self.player.pos):
            if re.search(item.pattern, itemName):
                self.board.removeItem(item)
                self.player.addItem(item)
                print(item.takeMsg)
                found = True

        if not found:
            print("You don't see a %s here." % itemName)

    def doInventory(self):
        items = self.player.inventory
        if len(items) == 0:
            print("You have nothing in your satchel. Not a stitch, not a squib. "
                  "A passing mouse scorns you in ill-disguised contempt.")
        else:
            print("Rooting through your battered satchel, you see:")
            for item in items:
                print("  %s" % item.name)

    def doMap(self):
        # TODO: consider ways to implement engine-modifying callbacks / overrides for magic items
        if self.player.hasItemName("Key of Admin"):
            self.board.dump(label="Administrator Map", admin=True)
        else:
            self.board.showTrail()

    def doSleep(self):
        print(random.choice(["Time passes...",
                             "You pause to contemplate the cruel impermanence of human existence.",
                             "Espying a passably pillow-shaped rock, you settle down for an impromptu siesta."]))

    def doHelp(self):
        print("I am but a feeble regex tree masquerading as an AI, but I understand a few basic constructs.\n\n"
              "Examples:\n"
              "  go north (or just 'n')\n"
              "  look\n"
              "  show map\n"
              "  inventory (or just 'i')\n"
              "  take the knife\n")

    def doDebug(self):
        self.board.dump(label="Sekret Map (U no see!)", admin=True)
