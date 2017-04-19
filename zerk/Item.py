class Item:

    def __init__(self, name, **kwargs):
        # required args
        self.name = name

        # defaults
        self.pos = None
        self.scoreValue = 20
        self.lookMsg = "You see a %s." % self.name

        # overrides
        self.__dict__.update(kwargs)
