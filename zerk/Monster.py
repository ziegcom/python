class Monster:

    def __init__(self, **kwargs):
        # defaults
        self.aggression = 0
        self.speed = 1
        self.pos = None
        self.alive = True

        # apply constructor overrides
        self.__dict__.update(kwargs)
