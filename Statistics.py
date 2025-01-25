import matplotlib.pyplot as plt
import time
import numpy as np


class Statistic:
    def __init__(self, start_time: time, board, flower_number):
        self.start_time = start_time
        self.num_of_flowers = flower_number
        self.times = [0]
        self.avg = []
        self.count_avg_distance(board)

    def count_avg_distance(self, board):
        count = 0
        sum_distances = 0
        hive = np.array((25, 25))
        for x in range(board.shape[0]):
            for y in range(board.shape[1]):
                if board[x][y] >= 1000:
                    b = np.array((x, y))
                    sum_distances += np.linalg.norm(hive - b)
                    count += 1
        if count == 0:
            self.avg.append(0)
        self.avg.append(sum_distances/count)

    def draw_plot(self, time_flower, board, number):
        if not self.num_of_flowers == number:
            self.num_of_flowers = int(np.sum(board >= 1000))
        else:
            return
        self.times.append(time_flower - self.start_time)

        print("---------------")
        print("Number of flowers stats: ", self.num_of_flowers)
        print("---------------")

        list_number = list(range(self.num_of_flowers, 21))
        list_number.reverse()
        k = 20 - self.num_of_flowers
        print("times: ", self.times)
        print("list_number: ", list_number)
        plt.plot(self.times, list_number, 'ro')
        plt.xlabel('time')
        plt.ylabel('number of flowers')
        #plt.savefig('flowers_per_time/plot_' + str(k))
        plt.show()

        plt.plot(self.times, list_number)
        plt.xlabel('time')
        plt.ylabel('number of flowers')
        plt.show()

        self.count_avg_distance(board)
        plt.plot(self.times, self.avg)
        plt.xlabel('time')
        plt.ylabel('average of distances flowers from hive')
        # plt.savefig('avg_per_time/plot_' + str(k))
        plt.show()




