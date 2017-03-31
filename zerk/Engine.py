import Board
import Player
import Monster

import re

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
                cmd = raw_input("What would you like to do? ")
                self.processCommand(cmd.lower())

    def processCommand(self, cmd):

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
        result = re.match(r"(take|get|grab|steal|filch|acquire|obtain|pick.*up)\s+(the|a|an\s+)?(\S+)", cmd)
        if result:
            itemName = result.group(3)
            return self.doTake(itemName)

        # inventory
        if re.search("inventory", cmd) or cmd == "i":
            return self.doInventory()

        # map
        if re.search("map", cmd):
            return self.doMap()

        # wait
        if re.search(r"wait|sleep|pause|delay", cmd):
            return self.doSleep()

        # debug
        if re.search("debug", cmd) and __debug__:
            return self.doDebug()

        # quit
        if re.search(r"quit|stop|kill (me|self|myself)", cmd):
            return self.endGame("You're a complete wuss. A waste of space. I've pushed out farts with more conviction than you.")

        # todo: drop/discard, attack/kill/slay, open, use, ...

        # otherwise
        print "I don't know how to %s.\n" % cmd

        self.confusion += 1
        if self.confusion > 2:
            self.doHelp()
            self.confusion = 0

    def proximityCheck(self):
        for monster in self.board.getMonsters():
            if monster.alive:
                # did the monster just get us?
                if monster.pos == self.player.pos:
                    print monster.loseMsg if hasattr(monster, 'loseMsg') else "You have been devoured by a %s." % monster.name
                    return self.endGame("You have died.")
                
                # emit spookiness
                dist = self.player.pos.dist(monster.pos)
                if dist <= 1.5:
                    print monster.nearMsg if hasattr(monster, 'nearMsg') else "You hear a loud clatter and gag on a strong stench in the air!"
                elif dist < 2.5:
                    print monster.medMsg if hasattr(monster, 'medMsg') else "You hear a scuttling nearby and the faint scraping of claws."
                elif dist < 3.5:
                    print monster.farMsg if hasattr(monster, 'farMsg') else "You hear a far-off howling in the darkness."
                
    def endGame(self, msg):
        # add points for anything in their inventory
        for item in self.player.inventory:
            self.player.score += item.scoreValue

        print '\n' + msg
        print "You have a score of %d points." % self.player.score
        self.gameOver = True

    ############################################################################
    #                                                                          #
    #                             Command Library                              #
    #                                                                          #
    ############################################################################

    def doWelcome(self):
        print "Welcome to Zerk, the command-line adventure game of your dreams!\n"

    def doLook(self):
        print("You are in a vast underground cavern, whose broken landscape is fractured "
              "by scattered impassable piles of riven rock and rubble.  There is no single "
              "light source, but a vague dimness emanates from the rotting and pestilant "
              "fungus that fibrously clings to the moldering stone.\n"
              "\n"
              "From the slowly-cooling pile of damp excreta in which you just stepped, "
              "you take it that you are not alone in this inpenetrable and sound-devouring "
              "darkness.\n")
        print ("You can go %s.\n" % self.board.listAvailableDirections(self.player.pos))

    def doMove(self, direction):
        pos = self.player.pos
        longDir = self.board.expandDirection(direction)

        if not self.board.canMove(pos, direction):
            print "The cavern wall prevents you from moving %s." % longDir
            return

        p2 = self.board.adjacentPos(pos, direction)
        if self.board.occupied(p2):
            print "You cannot move %s due to a towering mass of unscalable rubble." % longDir
            return

        print "You travel %s." % longDir
        self.player.pos = p2

        # any monsters here?
        for monster in self.board.getMonsters():
            if monster.pos == self.player.pos:
                if monster.alive:
                    print monster.winMsg if hasattr(monster, 'winMsg') else "You have defeated the %s!" % monster.name
                    self.player.score += monster.scoreValue
                    monster.alive = False
                else:
                    print monster.corpseMsg if hasattr(monster, 'corpseMsg') else "You see the corpse of a %s." % monster.name

        # any items here?
        for item in self.board.getItems(self.player.pos):
            print item.lookMsg if hasattr(item, 'lookMsg') else "You see a %s." % item.name

    def doTake(self, itemName):
        found = False
        for item in self.board.getItems(self.player.pos):
            if re.search(item.pattern, itemName):
                self.board.removeItem(item)
                self.player.addItem(item)
                print item.takeMsg if hasattr(item, 'takeMsg') else "You gingerly pick up the %s and place it lovely into your satchel." % item.name
                found = True

        if not found:
            print "You don't see a %s here." % itemName

    def doInventory(self):
        items = self.player.inventory
        if len(items) == 0:
            print("You have nothing in your satchel. Not a stich, not a squib. "
                  "A passing mouse scorns you in ill-disguised contempt.")
        else:
            print "Rooting through your battered satchel, you see:"
            for item in items:
                print "  %s" % item.name

    def doMap(self):
        if self.player.hasItemName("Key of Admin"):
            self.board.dump(label="Administrator Map", admin=True)
        else:
            self.board.showTrail()

    def doSleep(self):
        print random.choice(["Time passes...", 
                             "You pause to contemplate the cruel impermanence of human existence.",
                             "Espying a passably pillow-shaped rock, you settle down for an impromptu siesta."])

    def doHelp(self):
        print("I am but a feeble Python AI, but I understand a few basic constructs.\n"
              "Examples:\n"
              "  go north (or just 'n')\n"
              "  look\n"
              "  show map\n"
              "  inventory (or just 'i')\n"
              "  take the knife\n")

    def doDebug(self):
        self.board.dump(label="Sekret Map (U no see!)", admin=True)

    ############################################################################
    #                                                                          #
    #                             Utility Methods                              #
    #                                                                          #
    ############################################################################

