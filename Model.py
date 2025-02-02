import random

import numpy as np
import pygame
import time

from Bee import BeeStatus
from Hive import Hive
from Statistics import Statistic

START = 1
BLOCK_SIZE = 16
BLOCK_W_SPACE = BLOCK_SIZE + 1
BOARD_WIDTH = 50
BOARD_HEIGHT = 50

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
grey = (120, 120, 120)
orange = (30, 230, 55)

P_BORED_TO_SEARCH = 0.03
P_BORED_TO_FLYING_TO_FLOWER = 0.8
P_RESTING_TO_BORED = 0.3
P_DANCING_TO_RESTING = 0.1


def decision(probability) -> bool:
    return random.random() < probability


def rand_destination():
    x = np.random.randint(0, BOARD_WIDTH)
    y = np.random.randint(0, BOARD_HEIGHT)
    return (x, y)


def draw_grid(screen, width):
    for i in range(51):
        # vertical
        pygame.draw.line(screen, white, (i * BLOCK_W_SPACE + START, START), (i * BLOCK_W_SPACE + START, 851), 1)

    for i in range(1, 51):
        pygame.draw.line(screen, white, (START, i * BLOCK_W_SPACE + START), (851, i * BLOCK_W_SPACE + START), 1)


def draw_flowers(screen, board, flower_imgs):
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] >= 1000:
                flower_size = int(board[x][y] / 1000)
                screen.blit(flower_imgs[flower_size], (x * BLOCK_W_SPACE + START, y * BLOCK_W_SPACE + START))


def draw_board(board, screen, width, bee_img, hive_img):
    draw_grid(screen, width)
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i][j] == 200:
                screen.blit(hive_img, ((i - 1) * BLOCK_W_SPACE + START, (j - 1) * BLOCK_W_SPACE + START))
                # pygame.draw.rect(screen, red, (i * BLOCK_W_SPACE + START, j * BLOCK_W_SPACE + START, 16, 16))
            elif board[i][j] > 0 and board[i][j] < 1000 and board[i][j] != 200:
                screen.blit(bee_img, (i * BLOCK_W_SPACE + START, j * BLOCK_W_SPACE + START))


def find_bee_by_id(bees, id_):
    filtered = filter(lambda x: x.id == id_, bees)

    # print(filtered)
    return list(filtered)[0]


def scan(board, new_board, i, j, stats, bees):
    gained_memory = []
    for n in range(-2, 3):
        for m in range(-2, 3):
            try:
                if board[i + n][j + m] >= 1000:
                    new_board[i + n][j + m] = board[i + n][j + m] - 1000
                    #board[i + n][j + m] = board[i + n][j + m] - 1000
                    count_2 = np.sum(board >= 1000)

                    stats.draw_plot(time.time(), board.copy(), count_2)
                    return [i + n, j + m], []
                elif 0 < board[i + n][j + m] < 200:
                    bee_id = board[i + n, j + m]
                    neighbour_bee = find_bee_by_id(bees, bee_id)

                    if neighbour_bee.status == BeeStatus.DANCING:
                        gained_memory.append(neighbour_bee.memory[-1])
            except Exception as e:
                print(f"Błąd: {e}")
                continue
    return None, gained_memory


def bee_move(dest, i, j):
    move = [0, 0]
    if dest[0] > i:
        move[0] = 1
    elif dest[0] < i:
        move[0] = -1

    if dest[1] > j:
        move[1] = 1
    elif dest[1] < j:
        move[1] = -1

    return move


def find_new_destination():
    s = np.random.randint(50, size=1)
    t = np.random.randint(50, size=1)
    g = list(zip(s, t))

    dest = g[0]
    return dest


def process(board, bees, hive: Hive, stats: Statistic):
    new_board = np.zeros((800, 800), dtype=int)

    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i][j] == 200:
                new_board[i][j] = 200
            elif board[i][j] >= 1000:
                new_board[i][j] = board[i][j]

    for i in range(board.shape[0]):
        for j in range(board.shape[1]):

            if 0 < board[i][j] < 100:
                bee = find_bee_by_id(bees, board[i][j])

                flower, new_memory = scan(board, new_board, i, j, stats, bees)

                bee.memory.extend(new_memory)
                bee.memory = list(set(bee.memory))

                # if flower is not None:
                #     print('dance')
                #     bee.destination = (i, j)
                #     bee.dance = True
                #     if (flower[0], flower[1]) not in bee.memory:
                #         bee.memory.append((flower[0], flower[1]))


                dest = bee.destination

                # if dest == (i, j) and not bee.status == BeeStatus.DANCING:
                #     if not bee.memory:
                #         dest = find_new_destination()
                #         print(dest)
                #         bee.destination = dest

                move = bee_move(dest, i, j)
                if new_board[i + move[0]][j + move[1]] == 0:
                    new_board[i + move[0]][j + move[1]] = board[i][j]
                else:
                    (x, y) = (i, j)
                    x += random.randint(-1, 1)
                    y += random.randint(-1, 1)
                    if new_board[x][y] == 0:
                        new_board[x][y] = board[i][j]
                    else:
                        new_board[i][j] = board[i][j]

                if bee.status == BeeStatus.RETURNING_TO_HIVE and i in range(hive.x - 2, hive.x + 3) and j in range(hive.y - 2, hive.y + 3):
                    hive.get_inside(bee)
                    new_board[i][j] = 0
                    break

                if flower is not None:
                    print(f"Bee {bee.id} found flower at {flower}, returning to hive")
                    bee.status = BeeStatus.RETURNING_TO_HIVE
                    bee.destination = (hive.x, hive.y)
                    bee.memory.append((flower[0], flower[1]))
                    break

                # if bee.status is BeeStatus.BORED:
                #     print(f"Bee {bee.id} is bored?, returning to hive")
                #     bee.status = BeeStatus.RETURNING_TO_HIVE
                #     bee.destination = (hive.x, hive.y)
                #     break

                if bee.status == BeeStatus.SEARCHING and (i,j) == bee.destination:
                    print(f"Bee {bee.id} did not found a flower :(, trying again")
                    bee.destination = rand_destination()
                    break


    for bee in hive.bees:
        if bee.status == BeeStatus.BORED:
            if decision(P_BORED_TO_SEARCH):
                hive.go_outside(bee, new_board)
                bee.status = BeeStatus.SEARCHING
                bee.destination = rand_destination()
                print(f"Bee {bee.id} is searching for flowers at {bee.destination}!")
                break

        # if bee.status == BeeStatus
        if bee.status == BeeStatus.BORED:
            for hive_bee in hive.bees:
                if hive_bee.status == BeeStatus.DANCING and decision(P_BORED_TO_FLYING_TO_FLOWER):
                    bee.status = BeeStatus.SEARCHING
                    bee.destination = hive_bee.memory[-1]
                    hive_bee.status = BeeStatus.RESTING
                    hive.go_outside(bee, new_board)
                    print(f"Bee {bee.id} saw bee {hive_bee.id} dance and goes for flower {bee.destination}!")
                    break

        if bee.status == BeeStatus.RESTING:
            if decision(P_RESTING_TO_BORED):
                bee.status = BeeStatus.BORED
                print(f"Bee {bee.id} rested. Its bored.")
                break

        if bee.status == BeeStatus.DANCING:
            if decision(P_DANCING_TO_RESTING):
                bee.status = BeeStatus.RESTING
                print(f"Bee {bee.id} is tired of dancing. Resting.")
                break

        if bee.status == BeeStatus.SEARCHING:
            bee.status = BeeStatus.BORED

    return new_board
