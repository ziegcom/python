class Player:

    def __init__(self, **kwargs):
        # defaults
        self.pos = None
        self.alive = True
        self.score = 0
        self.inventory = set() # dictionary would be faster for frequent lookups

        # overrides
        self.__dict__.update(kwargs)

    def addItem(self, item):
        self.inventory.add(item)

    def hasItemName(self, itemName):
        for item in self.inventory:
            if item.name == itemName:
                return True
