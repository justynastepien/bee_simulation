from Bee import BeeStatus
import random


class Hive:

    def __init__(self, x, y):
        self.bees = []
        self.x = x
        self.y = y

    def add_bee(self, bee):
        self.bees.append(bee)

    def go_outside(self, bee, board):
        # rx = random.randint(-1, 1)
        # ry = random.randint(-1, 1)
        rx = 1
        ry = 0

        if board[self.x + rx, self.y + ry] != 0:
            print(f"Bee {bee.id}: No space to go outside!")
            return
        self.bees.remove(bee)
        board[self.x + rx, self.y + ry] = bee.id

    def get_inside(self, bee):
        print(f"Bee {bee.id} returned to hive. LETS DANCE!")
        bee.status = BeeStatus.DANCING
        self.bees.append(bee)
