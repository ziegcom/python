class Item:

    def __init__(self, **kwargs):
        # defaults
        self.pos = None

        # overrides
        self.__dict__.update(kwargs)
