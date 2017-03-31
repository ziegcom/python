class Item:

    def __init__(self, **kwargs):
        # defaults
        self.pos = None
        self.scoreValue = 20

        # overrides
        self.__dict__.update(kwargs)
