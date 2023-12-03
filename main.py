import sys
from pathlib import Path
import csv
import yaml

import pygame
from pygame.locals import *
import time
import numpy as np
import Model
from Hive import Hive
from Bee import Bee

DUMP_LOCATION = Path("dump")
FILENAME_BOARD = DUMP_LOCATION / "board.csv"
FILENAME_BEES = DUMP_LOCATION / "bees.yml"
FILENAME_HIVE = DUMP_LOCATION / "hive.yml"

MAX_FLOWER_SIZE = 10
DEFAULT_FLOWER_SIZE = (16, 16)


class Application:

    def __init__(self):
        (self.width, self.height) = (852, 852)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Bees Simulation")
        self.bg_img = pygame.image.load(Path('assets/grass.jpg'))
        self.bg_img = pygame.transform.scale(self.bg_img, (852, 852))

        self.hive_img = pygame.image.load(Path('assets/hive.png'))
        self.hive_img = pygame.transform.scale(self.hive_img, (58, 58)) #60x60

        self.flower_img = pygame.image.load(Path('assets/flower.png'))
        self.flower_img = pygame.transform.scale(self.flower_img, DEFAULT_FLOWER_SIZE)
        self.flower_imgs = []
        self.generate_flower_images()

        self.bee_img = pygame.image.load(Path('assets/bee.png'))
        self.bee_img = pygame.transform.scale(self.bee_img, (16, 16))
        self.updateTime = 0.05

        self.running = True

        self.running_time = 0

        self.board = np.zeros((800, 800))
        self.pick_flowers()

        self.board[25][25] = 200 #hive token
        self.hive = Hive(25, 25)
        self.bees = []
        self.create_bees()

        self.draw_model()
        self.run()

    def draw_model(self):
        self.screen.blit(self.bg_img, (0, 0))

        Model.draw_flowers(self.screen, self.board, self.flower_imgs)
        Model.draw_board(self.board, self.screen, 800, self.bee_img, self.hive_img)

        pygame.display.flip()
        start = time.time()

    def pick_flowers(self):
        p = np.random.randint(50, size=20)
        r = np.random.randint(50, size=20)
        f = list(zip(p, r))

        for i in f:
            flower_size = np.random.randint(1, 10) * 1000

            if self.board[i[0]][i[1]] == 200:
                z = 1
                while z < 400:
                    if self.board[i[0]+z][i[1]] == 0:
                        self.board[i[0]][i[1]] = flower_size
                        break
            else:
                # 100 flower token
                self.board[i[0]][i[1]] = flower_size

        return f
    
    def generate_flower_images(self):
        for i in range(MAX_FLOWER_SIZE):
            new_size = (int(DEFAULT_FLOWER_SIZE[0] * (1 + i*0.2)), int(DEFAULT_FLOWER_SIZE[1] * (1 + i*0.2)))
            print(new_size)
            self.flower_imgs.append(pygame.transform.scale(self.flower_img, new_size))


    def create_bees(self, size=30):
        # p = np.random.randint(50, size=size)
        # r = np.random.randint(50, size=size)
        # f = list(zip(p, r))

        # s = np.random.randint(50, size=size)
        # t = np.random.randint(50, size=size)
        # g = list(zip(s, t))
        # print(f)
        for i in range(size):
            print(i)
            bee = Bee(i+1)
            # bee.destination = g[i]
            self.bees.append(bee)
            self.hive.add_bee(bee)
            # self.board[f[i][0]][f[i][1]] = i+1


    def dump_data(self):
        print("---DUMPING DATA...")
        DUMP_LOCATION.mkdir(exist_ok=True)
        with open(FILENAME_BOARD, mode="w") as f:
            writer = csv.writer(f)
            writer.writerows(self.board)
        with open(FILENAME_BEES, mode="w") as f:
            yaml.dump(self.bees, f)
        with open(FILENAME_HIVE, mode="w") as f:
            yaml.dump(self.hive, f)
        print("---DATA DUMPED")


    def manage_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                pygame.event.clear()
                while True:
                    event = pygame.event.wait()
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            break
                        if event.key == K_RIGHT:
                            newevent = pygame.event.Event(pygame.locals.KEYDOWN, unicode="", key=K_SPACE,
                                                          mod=pygame.locals.KMOD_NONE)
                            pygame.event.post(newevent)
                            break
                        if event.key == K_s:
                            self.dump_data()

    def run(self):
        while self.running:
            self.board = Model.process(self.board, self.bees, self.hive)

            self.draw_model()

            time.sleep(self.updateTime)
            self.manage_keys()

            self.running_time += 1


app = Application()
app.run()
