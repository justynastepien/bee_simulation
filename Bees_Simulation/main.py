import sys

import pygame
from pygame.locals import *
import time
import numpy as np
import Model
from Hive import Hive
from Bee import Bee


class Application:

    def __init__(self):
        (self.width, self.height) = (852, 852)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Bees Simulation")
        self.bg_img = pygame.image.load('grass.jpg')
        self.bg_img = pygame.transform.scale(self.bg_img, (852, 852))

        self.hive_img = pygame.image.load('hive.png')
        self.hive_img = pygame.transform.scale(self.hive_img, (58, 58)) #60x60

        self.flower_img = pygame.image.load('flower.png')
        self.flower_img = pygame.transform.scale(self.flower_img, (16, 16))

        self.bee_img = pygame.image.load('bee.png')
        self.bee_img = pygame.transform.scale(self.bee_img, (16, 16))
        self.updateTime = 0.5

        self.running = True

        self.running_time = 0

        self.board = np.zeros((800, 800))
        self.flowers = self.pick_flowers()

        self.bees = []
        self.create_bees()

        self.board[25][25] = 200 #hive token

        self.hive = Hive(self.bees)

        self.draw_model()
        self.run()

    def draw_model(self):
        self.screen.blit(self.bg_img, (0, 0))

        Model.draw_flowers(self.screen, self.flowers, self.flower_img)
        Model.draw_board(self.board, self.screen, 800, self.bee_img, self.hive_img)

        pygame.display.flip()
        start = time.time()

    def pick_flowers(self):
        p = np.random.randint(50, size=20)
        r = np.random.randint(50, size=20)
        f = list(zip(p, r))

        for i in f:

            if self.board[i[0]][i[1]] == 200:
                z = 1
                while z < 400:
                    if self.board[i[0]+z][i[1]] == 0:
                        self.board[i[0]][i[1]] = 100
                        break
            else:
                # 100 flower token
                self.board[i[0]][i[1]] = 100

        return f

    def create_bees(self, size=30):
        p = np.random.randint(50, size=size)
        r = np.random.randint(50, size=size)
        f = list(zip(p, r))

        s = np.random.randint(50, size=size)
        t = np.random.randint(50, size=size)
        g = list(zip(s, t))
        print(f)
        for i in range(size):
            print(i)
            bee = Bee(i+1)
            bee.destination = g[i]
            self.bees.append(bee)
            self.board[f[i][0]][f[i][1]] = i+1

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

    def run(self):
        while self.running:
            self.board = Model.process(self.board, self.flowers, self.bees, self.hive)

            self.draw_model()

            time.sleep(self.updateTime)
            self.manage_keys()

            self.running_time += 1


app = Application()
