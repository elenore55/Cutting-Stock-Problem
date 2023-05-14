from random import shuffle, randint, choices, sample
from copy import deepcopy
from math import sqrt
import matplotlib.pyplot as plt
from data_reader import DataReader


class EP_Optimizer(object):

    def __init__(self):
        self.MAX_ITERATIONS = 1000
        self.POPULATION_SIZE = 100
        self.stock_length = None
        self.demand = []

    def generate_initial_population(self):
        population = []
        for _ in range(self.POPULATION_SIZE):
            shuffle(self.demand)
            population.append(deepcopy(self.demand))
        return population

    def calculate_cost(self, chromosome):
        stocks = self.get_stocks_from_chromosome(chromosome)
        num_stocks = len(stocks)
        wastage_arr = [self.stock_length - sum(stock) for stock in stocks]
        V_arr = [int(waste > 0) for waste in wastage_arr]
        w_sum = sum(sqrt(wastage_arr[i] / self.stock_length) for i in range(num_stocks))
        V_sum = sum(V_arr[i] / num_stocks for i in range(num_stocks))
        return (w_sum + V_sum) / (num_stocks + 1)

    def get_stocks_from_chromosome(self, chromosome):
        stocks = []
        stock = []
        stock_sum = 0
        for gene in chromosome:
            if stock_sum + gene <= self.stock_length:
                stock_sum += gene
                stock.append(gene)
            else:
                stocks.append(stock)
                stock = [gene]
                stock_sum = gene
        if len(stock) > 0:
            stocks.append(stock)
        return stocks

    def generate_child(self, chromosome, repeat=2):
        child = deepcopy(chromosome)
        for _ in range(repeat):
            ind1 = randint(0, len(child) - 1)
            stocks = self.get_stocks_from_chromosome(child)
            probabilities = self.calculate_stocks_probabilities(stocks)
            chosen_stocks = choices(stocks, weights=probabilities, k=2)
            stock1_ind = stocks.index(chosen_stocks[0])
            stock2_ind = stocks.index(chosen_stocks[1])
            ind2_in_stock = randint(0, len(chosen_stocks[0]) - 1)
            ind3_in_stock = randint(0, len(chosen_stocks[1]) - 1)
            ind2 = ind3 = 0
            for i in range(stock1_ind):
                ind2 += len(stocks[i])
            ind2 += ind2_in_stock
            for i in range(stock2_ind):
                ind3 += len(stocks[i])
            ind3 += ind3_in_stock
            child[ind1], child[ind2] = child[ind2], child[ind1]
            child[ind1], child[ind3] = child[ind3], child[ind1]
        return child

    def calculate_stocks_probabilities(self, stocks):
        wastage_arr = [self.stock_length - sum(stock) for stock in stocks]
        w_sum = sum(sqrt(1 / w) for w in wastage_arr if w > 0)
        return [sqrt(1 / waste) / w_sum if waste > 0 else 0 for waste in wastage_arr]

    def tournament(self, all_chromosomes):
        Q = 10
        num_wins = [[ch, 0] for ch in all_chromosomes]
        costs = [self.calculate_cost(ch) for ch in all_chromosomes]
        for i in range(len(all_chromosomes)):
            possible_opponents = all_chromosomes[:i] + all_chromosomes[i + 1:]
            opponents_costs = costs[:i] + costs[i + 1:]
            opponents_indices = sample(range(len(possible_opponents)), Q)
            for ind in opponents_indices:
                if costs[i] < opponents_costs[ind]:
                    num_wins[i][1] += 1
        num_wins.sort(key=lambda x: x[1], reverse=True)
        return [num_wins[i][0] for i in range(self.POPULATION_SIZE)]

    def optimize(self, problem_path, queue=None):
        self.demand = []
        self.stock_length, l_arr, d_arr = DataReader.read(problem_path)
        for i in range(len(l_arr)):
            self.demand.extend([l_arr[i]] * d_arr[i])
        population = self.generate_initial_population()
        iter_cnt = 0
        num_iters_same_result = 0
        last_result = float('inf')
        results = []
        while True:
            iter_cnt += 1
            children = []
            for chromosome in population:
                children.append(self.generate_child(chromosome))
            population = deepcopy(self.tournament(population + children))
            least_cost_for_iter = self.calculate_cost(population[0])
            results.append(least_cost_for_iter)
            if abs(least_cost_for_iter - last_result) < 0.00001:
                num_iters_same_result += 1
            else:
                num_iters_same_result = 0
            last_result = least_cost_for_iter

            if least_cost_for_iter == 0 or iter_cnt > self.MAX_ITERATIONS or num_iters_same_result >= 30:
                solution = population[0]
                stocks = self.get_stocks_from_chromosome(solution)
                print('ITERATION')
                print(iter_cnt)
                print('COST')
                print(least_cost_for_iter)
                print('NUMBER OF STOCKS')
                print(len(stocks))
                break
        plt.plot(range(1, len(results) + 1), results)
        plt.xlabel('Iteration')
        plt.ylabel('Best result')
        plt.show()
        if queue is not None:
            queue.put((self.stock_length, l_arr, d_arr, stocks))
        return self.stock_length, l_arr, d_arr, stocks


if __name__ == '__main__':
    optimizer = EP_Optimizer()
    optimizer.optimize('data/problem3.txt')
