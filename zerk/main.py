#!/usr/bin/env python

from Board   import Board
from Monster import Monster 
from Item    import Item
from Player  import Player 
from Engine  import Engine

import sys

def main():
    # instantiate a 20x20 grid
    board = Board(20)

    # scatter some random obstacles about the board    
    board.createObstacles(8, 8)

    # instantiate a monster
    m1 = Monster(speed = 2,
                 char = "T",
                 aggression = 2,
                 scoreValue = 1000,
                 name = "Thessalhydra",
                 farMsg  = "You hear the clanking of distant chains.",
                 medMsg  = "You hear the rattle of a dragged chain and sense a fouling of the air.",
                 nearMsg = "You hear a sudden loud clangor and gag on a horrid gangrene stench.",
                 winMsg  = "You stand over the mishapen nightmarish carcass of the slain Thessalhydra, "
                           "and all humanity sings your praises for ridding the Earth of such a malign "
                           "stain on nature's bounty.",
                 loseMsg = "The Thessalhydra lunges past your defenses, ripping off your head with its "
                           "many-toothed jaws and shredding your body with its uncounted claws.  It "
                           "howls in gluttonous victory and then proceeds to lap at your still-steaming "
                           "entrails.")

    m2 = Monster(name = "mouse", 
                 nearMsg = "You hear a squeaking down near the ground.", 
                 winMsg  = "You clumsily step on the mouse's tail, causing it to stiffen in fright and feign death until you go away.",
                 scoreValue = 2)

    m3 = Monster(name = "Cave-Bat", 
                 aggression = 1,
                 medMsg  = "You hear a distant fluttering as of torn canvas sails.",
                 nearMsg = "You hear a nearly infra-sonic screeching high above, and taste the rancid spoor of hot demon breath.",
                 winMsg  = "With a leap you tear the Cave-Bat from the air, wrenching it to earth and crushing its withered wings.",
                 loseMsg = "Suddenly a demonic shape hurls screaming from the heights, poison talons gouging your eyes while its fangs tear fleshy chunks from your throat.",
                 scoreValue = 300)

    # place monsters on the board
    board.addMonster(m1)
    board.addMonster(m2)
    board.addMonster(m3)

    # place items on the board
    thing1 = Item(name       = "Key of Admin",
                  pattern    = "key",
                  weight     = 5,
                  cost       = 500,
                  scoreValue = 200,
                  lookMsg    = "You see a gleaming silver key, fully a foot long and glowing with a shimmery "
                               "nimbus of power, lying forelorn on the dusty cavern floor.",
                  takeMsg    = "You hold aloft the mighty Key of Admin, and feel a shiver of power ripple "
                               "down your arm.  Suddenly you feel an enhanced awareness of your surroundings.")
    thing2 = Item(name = "suspicious fungus",
                  pattern = "fungus|fungi|fungoid|lichen",
                  weight = 2,
                  cost = 5,
                  scoreValue = 10,
                  lookMsg = "You see a suspicious-looking fungus growing on the rocks nearby.",
                  takeMsg = "Heaven knows what you plan to do with it, but you carefully nestle the mottled fungoid into your bag.")

    thing3 = Item(name = "rock resembling Donald Trump's hairpiece",
                  pattern = "rock|trump|hair",
                  weight = 10,
                  cost = 1,
                  scoreValue = 15,
                  lookMsg = "You see a curious-looking rock that looks like nothing so much as Donald Trump's disembodied hairpiece.",
                  takeMsg = "You distractedly drop the rock into your bag, hoping beyond hope for the chance to return it...with vigor.")

    board.addItem(thing1)
    board.addItem(thing2)
    board.addItem(thing3)

    # instantiate the player character
    player = Player(name = "Melvin")

    # place player somewhere on the board
    board.addPlayer(player)

    board.dump(label="Debugging", admin=True)

    # start a game session
    engine = Engine(board, player)
    engine.start()

sys.exit(main())
