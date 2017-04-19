class Monster:

    def __init__(self, name, **kwargs):
        # required args
        self.name       = name

        # defaults
        self.pos        = None
        self.alive      = True
        self.aggression = 0
        self.speed      = 1
        self.scoreValue = 10
        self.nearMsg    = "You hear a loud clatter and gag on a strong stench in the air!"
        self.medMsg     = "You hear a scuttling nearby and the faint scraping of claws."
        self.farMsg     = "You hear a far-off howling in the darkness."
        self.winMsg     = "You have defeated the %s!" % self.name
        self.loseMsg    = "You have been devoured by a %s." % self.name
        self.corpseMsg  = "You see the corpse of a %s." % self.name

        # apply constructor overrides
        self.__dict__.update(kwargs)

        # post-processing (after overrides)
        self.origAggression = self.aggression
