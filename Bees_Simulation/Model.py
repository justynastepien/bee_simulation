import pygame
import numpy as np

from Bee import Bee
from Hive import Hive

START = 1
BLOCK_SIZE = 16
BLOCK_W_SPACE = BLOCK_SIZE + 1

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
grey = (120, 120, 120)
orange = (30, 230, 55)

light_color = red
car_color = blue
bus_color = orange
empty_color = grey


def draw_grid(screen, width):
    for i in range(51):
        # vertical
        pygame.draw.line(screen, white, (i * BLOCK_W_SPACE + START, START), (i * BLOCK_W_SPACE + START, 851), 1)

    for i in range(1, 51):
        pygame.draw.line(screen, white, (START, i * BLOCK_W_SPACE + START), (851, i * BLOCK_W_SPACE + START), 1)


def draw_flowers(screen, flowers, flower_img):
    for cords in flowers:
        screen.blit(flower_img, (cords[0] * BLOCK_W_SPACE + START, cords[1] * BLOCK_W_SPACE + START))


def draw_board(board, screen, width, bee_img, hive_img):
    draw_grid(screen, width)
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i][j] == 200:
                screen.blit(hive_img, ((i - 1) * BLOCK_W_SPACE + START, (j - 1) * BLOCK_W_SPACE + START))
                # pygame.draw.rect(screen, red, (i * BLOCK_W_SPACE + START, j * BLOCK_W_SPACE + START, 16, 16))
            elif board[i][j] != 0 and board[i][j] != 100:
                screen.blit(bee_img, (i * BLOCK_W_SPACE + START, j * BLOCK_W_SPACE + START))


def find_bee_by_id(bees, id):
    filtered = filter(lambda x: x.id == id, bees)

    print(filtered)
    return list(filtered)[0]


def scan(board, i, j):
    for n in range(-2, 2):
        for m in range(-2, 2):
            try:
                if board[i + n][j + m] == 100:
                    return [i + n, j + m]
            except:
                continue
    return None


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


def process(board, flowers, bees, hive: Hive):
    new_board = np.zeros((800, 800))
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):

            if board[i][j] == 200:
                new_board[i][j] = 200
                continue
            elif board[i][j] == 100:
                new_board[i][j] = 100
                continue
            elif 0 < board[i][j] < 100:

                bee = find_bee_by_id(bees, board[i][j])

                flower = scan(board, i, j)

                if flower is not None:
                    print('dance')
                    bee.destination = (i, j)
                    bee.dance = True
                    if (flower[0], flower[1]) not in bee.memory:
                        bee.memory.append((flower[0], flower[1]))

                dest = bee.destination

                if dest == (i, j) and not bee.dance:
                    if not bee.memory:
                        dest = find_new_destination()
                        print(dest)
                        bee.destination = dest

                move = bee_move(dest, i, j)
                if board[i + move[0]][j + move[1]] == 0:
                    new_board[i + move[0]][j + move[1]] = board[i][j]
                else:
                    new_board[i][j] = board[i][j]

    return new_board
