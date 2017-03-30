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
                 aggression = 1,    
                 name    = "Thessalhydra",
                 char    = "T",
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

    # place monster somewhere on the board
    board.addMonster(m1)

    # place an item somewhere on the board
    item = Item(name    = "Key of Admin",
                pattern = "key",
                weight  = 5,
                cost    = 500,
                points  = 200,
                lookMsg = "You see a gleaming silver key, fully a foot long and glowing with a shimmery "
                          "nimbus of power, lying forelorn on the dusty cavern floor.",
                takeMsg = "You hold aloft the mighty Key of Admin, and feel a shiver of power ripple "
                          "down your arm.  Suddenly you feel an enhanced awareness of your surroundings.")
    board.addItem(item)

    # instantiate the player character
    player = Player(name = "Melvin")

    # place player somewhere on the board
    board.addPlayer(player)

    board.dump(label="Debugging", admin=True)

    # start a game session
    engine = Engine(board, player)
    engine.start()

sys.exit(main())
