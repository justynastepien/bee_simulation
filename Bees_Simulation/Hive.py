class Hive:

    def __init__(self, bees: []):
        self.bees = bees

    def add_bee(self, bee):
        self.bees.append(bee)

    def remove_bee(self, bee):
        self.bees.remove(bee)
