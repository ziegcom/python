class Monster:

    def __init__(self, **kwargs):
        # defaults
        self.aggression = 0
        self.speed = 1
        self.pos = None
        self.alive = True
        self.scoreValue = 10

        # apply constructor overrides
        self.__dict__.update(kwargs)

        # keep a backup so we can dynamically tweak this
        self.origAggression = self.aggression
