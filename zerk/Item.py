class Item:

    def __init__(self, name, **kwargs):
        # defaults
        self.name = name
        self.pos = None
        self.scoreValue = 20

        # overrides
        self.__dict__.update(kwargs)

        # default attributes which reference other attributes
        if not hasattr(self, 'lookMsg'):
            self.lookMsg = "You see a %s." % self.name
