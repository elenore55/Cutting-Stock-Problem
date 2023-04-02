from random import shuffle, randint, choices, sample
from copy import deepcopy
from math import sqrt

L = 10
l_arr = [4, 3, 2]
d_arr = [50, 30, 35]
MAX_ITERATIONS = 100
POPULATION_SIZE = 50


def generate_initial_population(demand):
    population = []
    for _ in range(POPULATION_SIZE):
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


def generate_child(chromosome, repeat=2):
    child = deepcopy(chromosome)
    for _ in range(repeat):
        ind1 = randint(0, len(child) - 1)
        stocks = get_stocks_from_chromosome(child)
        probabilities = calculate_stocks_probabilities(stocks)
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


def calculate_stocks_probabilities(stocks):
    probabilities = []
    wastage_arr = [L - sum(stock) for stock in stocks]
    w_sum = sum(sqrt(1 / w) for w in wastage_arr if w > 0)
    for i in range(len(stocks)):
        if wastage_arr[i] == 0:
            probabilities.append(0)
        else:
            probabilities.append(sqrt(1 / wastage_arr[i]) / w_sum)
    return probabilities


def tournament(all_chromosomes):
    q = 5
    num_wins = [[ch, 0] for ch in all_chromosomes]
    costs = [calculate_cost(ch) for ch in all_chromosomes]
    for i in range(len(all_chromosomes)):
        possible_opponents = all_chromosomes[:i] + all_chromosomes[i + 1:]
        opponents_costs = costs[:i] + costs[i + 1:]
        opponents_indices = sample(range(len(possible_opponents)), q)
        for ind in opponents_indices:
            if costs[i] < opponents_costs[ind]:
                num_wins[i][1] += 1
    num_wins.sort(key=lambda x: x[1], reverse=True)
    return [num_wins[i][0] for i in range(POPULATION_SIZE)]


def main():
    demand = []
    for i in range(len(l_arr)):
        demand.extend([l_arr[i]] * d_arr[i])
    population = generate_initial_population(demand)

    iter_cnt = 0
    while True:
        iter_cnt += 1
        children = []
        for chromosome in population:
            children.append(generate_child(chromosome))

        population = deepcopy(tournament(population + children))
        least_cost_for_iter = calculate_cost(population[0])
        stocks = get_stocks_from_chromosome(population[0])

        if iter_cnt > MAX_ITERATIONS:
            print('SOLUTION')
            print(population[0])
            print('COST')
            print(least_cost_for_iter)
            print('NUMBER OF STOCKS')
            print(len(stocks))
            break


if __name__ == '__main__':
    main()
