class Monster:

    def __init__(self, **kwargs):
        # defaults
        self.name       = "grue"
        self.pos        = None
        self.alive      = True
        self.aggression = 0
        self.speed      = 1
        self.scoreValue = 10
        self.nearMsg    = "You hear a loud clatter and gag on a strong stench in the air!"
        self.medMsg     = "You hear a scuttling nearby and the faint scraping of claws."
        self.farMsg     = "You hear a far-off howling in the darkness."

        # apply constructor overrides
        self.__dict__.update(kwargs)

        # finally, apply defaults that reference other potentially-overridden attributes
        self.origAggression = self.aggression
        if not hasattr(self, 'winMsg'):
            self.winMsg = "You have defeated the %s!" % self.name
        if not hasattr(self, 'loseMsg'):
            self.loseMsg = "You have been devoured by a %s." % self.name
        if not hasattr(self, 'corpseMsg'):
            self.corpseMsg = "You see the corpse of a %s." % self.name
