from random import shuffle, randint, choices, sample
from copy import deepcopy
from math import sqrt
import matplotlib.pyplot as plt

MAX_ITERATIONS = 1000
POPULATION_SIZE = 100


def generate_initial_population(demand):
    population = []
    for _ in range(POPULATION_SIZE):
        shuffle(demand)
        population.append(deepcopy(demand))
    return population


def calculate_cost(chromosome, stock_length):
    stocks = get_stocks_from_chromosome(chromosome, stock_length)
    num_stocks = len(stocks)
    wastage_arr = [stock_length - sum(stock) for stock in stocks]
    V_arr = [int(waste > 0) for waste in wastage_arr]
    w_sum = sum(sqrt(wastage_arr[i] / stock_length) for i in range(num_stocks))
    V_sum = sum(V_arr[i] / num_stocks for i in range(num_stocks))
    return (w_sum + V_sum) / (num_stocks + 1)


def generate_child(chromosome, stock_length, repeat=2):
    child = deepcopy(chromosome)
    for _ in range(repeat):
        ind1 = randint(0, len(child) - 1)
        stocks = get_stocks_from_chromosome(child, stock_length)
        probabilities = calculate_stocks_probabilities(stocks, stock_length)
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


def get_stocks_from_chromosome(chromosome, stock_length):
    stocks = []
    stock = []
    stock_sum = 0
    for gene in chromosome:
        if stock_sum + gene <= stock_length:
            stock_sum += gene
            stock.append(gene)
        else:
            stocks.append(stock)
            stock = [gene]
            stock_sum = gene
    if len(stock) > 0:
        stocks.append(stock)
    return stocks


def calculate_stocks_probabilities(stocks, stock_length):
    wastage_arr = [stock_length - sum(stock) for stock in stocks]
    w_sum = sum(sqrt(1 / w) for w in wastage_arr if w > 0)
    return [sqrt(1 / waste) / w_sum if waste > 0 else 0 for waste in wastage_arr]


def tournament(all_chromosomes, stock_length):
    Q = 10
    num_wins = [[ch, 0] for ch in all_chromosomes]
    costs = [calculate_cost(ch, stock_length) for ch in all_chromosomes]
    for i in range(len(all_chromosomes)):
        possible_opponents = all_chromosomes[:i] + all_chromosomes[i + 1:]
        opponents_costs = costs[:i] + costs[i + 1:]
        opponents_indices = sample(range(len(possible_opponents)), Q)
        for ind in opponents_indices:
            if costs[i] < opponents_costs[ind]:
                num_wins[i][1] += 1
    num_wins.sort(key=lambda x: x[1], reverse=True)
    return [num_wins[i][0] for i in range(POPULATION_SIZE)]


def read_data(path):
    with open(path) as f:
        lines = f.readlines()
        stock_length = int(lines[0])
        l_arr = []
        d_arr = []
        for i in range(1, len(lines)):
            l, d = lines[i].split(',')
            l_arr.append(int(l))
            d_arr.append(int(d))
        return stock_length, l_arr, d_arr


def optimize(problem_path):
    demand = []
    stock_length, l_arr, d_arr = read_data(problem_path)
    for i in range(len(l_arr)):
        demand.extend([l_arr[i]] * d_arr[i])
    population = generate_initial_population(demand)

    iter_cnt = 0
    num_iters_same_result = 0
    last_result = float('inf')
    results = []
    while True:
        iter_cnt += 1
        children = []
        for chromosome in population:
            children.append(generate_child(chromosome, stock_length))
        population = deepcopy(tournament(population + children, stock_length))
        least_cost_for_iter = calculate_cost(population[0], stock_length)
        results.append(least_cost_for_iter)
        if abs(least_cost_for_iter - last_result) < 0.00001:
            num_iters_same_result += 1
        else:
            num_iters_same_result = 0
        last_result = least_cost_for_iter

        if least_cost_for_iter == 0 or iter_cnt > MAX_ITERATIONS or num_iters_same_result >= 30:
            solution = population[0]
            stocks = get_stocks_from_chromosome(solution, stock_length)
            print('ITERATION')
            print(iter_cnt)
            print('COST')
            print(least_cost_for_iter)
            print('NUMBER OF STOCKS')
            print(len(stocks))
            # schedule(stocks)
            # naive_scheduling(stocks)
            break
    plt.plot(range(1, len(results) + 1), results)
    plt.xlabel('Iteration')
    plt.ylabel('Best result')
    plt.show()
    return stock_length, l_arr, d_arr, stocks


if __name__ == '__main__':
    optimize('data/problem3.txt')
