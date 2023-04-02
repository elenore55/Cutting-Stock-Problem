from random import shuffle
from copy import deepcopy
from math import sqrt

L = 10
l_arr = [4, 3, 2]
d_arr = [5, 3, 3]


def generate_initial_population(num_chromosomes, demand):
    population = []
    for _ in range(num_chromosomes):
        shuffle(demand)
        population.append(deepcopy(demand))
    return population


def calculate_cost(chromosome):
    stocks = get_stocks_from_chromosome(chromosome)
    num_stocks = len(stocks)
    wastage_arr = []
    V_arr = []
    for stock in stocks:
        w = L - sum(stock)
        wastage_arr.append(w)
        V_arr.append(int(w > 0))
    w_sum = sum(sqrt(wastage_arr[i] / L) for i in range(num_stocks))
    V_sum = sum(V_arr[i] / num_stocks for i in range(num_stocks))
    return (w_sum + V_sum) / (num_stocks + 1)


def get_stocks_from_chromosome(chromosome):
    stocks = []
    stock = []
    stock_sum = 0
    for gene in chromosome:
        if stock_sum + gene <= L:
            stock_sum += gene
            stock.append(gene)
        else:
            stocks.append(stock)
            stock = [gene]
            stock_sum = gene
    if len(stock) > 0:
        stocks.append(stock)
    return stocks


def main():
    demand = []
    for i in range(len(l_arr)):
        demand.extend([l_arr[i]] * d_arr[i])
    population = generate_initial_population(10, demand)
    print(population)
    print(calculate_cost([4, 5, 2, 6, 2, 8]))


if __name__ == '__main__':
    main()
