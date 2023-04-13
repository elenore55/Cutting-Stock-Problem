from random import shuffle, randint, choices, sample
from copy import deepcopy
from math import sqrt

L = 10
l_arr = [4, 3, 2]
d_arr = [50, 30, 35]
MAX_ITERATIONS = 100
POPULATION_SIZE = 50
SIZE_CHANGED_COST = 7
STOCK_CHANGED_COST = 2


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


def generate_initial_scheduling_population(stocks):
    chromosome = get_scheduling_options(stocks)
    population = []
    for _ in range(POPULATION_SIZE):
        shuffle(chromosome)
        population.append(deepcopy(chromosome))
    return population


def get_scheduling_options(stocks):
    result = []
    for i, stock in enumerate(stocks):
        numbers = set(stock)
        for num in numbers:
            result.append((i, num))
    return result


def calculate_scheduling_cost(chromosome):
    cost = 0
    for i in range(1, len(chromosome)):
        previous = chromosome[i - 1]
        current = chromosome[i]
        if previous[0] != current[0]:
            cost += STOCK_CHANGED_COST
        if previous[1] != current[1]:
            cost += SIZE_CHANGED_COST
    return cost


def generate_scheduling_child(chromosome, repeat=2):
    child = deepcopy(chromosome)
    for _ in range(repeat):
        ind1 = randint(0, len(child) - 1)
        probabilities = calculate_cutting_probabilities(chromosome)
        chosen_indices = choices(range(len(child)), weights=probabilities, k=2)
        ind2 = chosen_indices[0]
        ind3 = chosen_indices[1]
        child[ind1], child[ind2] = child[ind2], child[ind1]
        child[ind1], child[ind3] = child[ind3], child[ind1]
    return child


def calculate_cutting_probabilities(chromosome):
    result = []
    count_of_same_adjacent = []
    for i, pair in enumerate(chromosome):
        size = pair[1]
        if i == 0 or size == chromosome[i - 1][1]:
            count = 1
            for j in range(i + 1, len(chromosome)):
                if chromosome[j][1] == size:
                    count += 1
                else:
                    break
            count_of_same_adjacent.append(count)
        else:
            count_of_same_adjacent.append(count_of_same_adjacent[-1])

    normalization_sum = sum(1 / i for i in count_of_same_adjacent)
    for i in count_of_same_adjacent:
        result.append(1 / (i * normalization_sum))
    return result


def scheduling_tournament(all_chromosomes):
    q = 5
    num_wins = [[ch, 0] for ch in all_chromosomes]
    costs = [calculate_scheduling_cost(ch) for ch in all_chromosomes]
    for i in range(len(all_chromosomes)):
        possible_opponents = all_chromosomes[:i] + all_chromosomes[i + 1:]
        opponents_costs = costs[:i] + costs[i + 1:]
        opponents_indices = sample(range(len(possible_opponents)), q)
        for ind in opponents_indices:
            if costs[i] < opponents_costs[ind]:
                num_wins[i][1] += 1
    num_wins.sort(key=lambda x: x[1], reverse=True)
    return [num_wins[i][0] for i in range(POPULATION_SIZE)]


def schedule(stocks):
    # for stock in stocks:
    #     stock.sort(reverse=True)
    #     print(stock)
    scheduling_population = generate_initial_scheduling_population(stocks)

    iter_cnt = 0
    while True:
        iter_cnt += 1
        children = []
        for chromosome in scheduling_population:
            children.append(generate_scheduling_child(chromosome))
        scheduling_population = deepcopy(scheduling_tournament(scheduling_population + children))
        if iter_cnt > MAX_ITERATIONS:
            solution = scheduling_population[0]
            print('COST')
            print(calculate_scheduling_cost(solution))
            break


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

        if iter_cnt > MAX_ITERATIONS:
            solution = population[0]
            stocks = get_stocks_from_chromosome(solution)
            print('COST')
            print(least_cost_for_iter)
            print('NUMBER OF STOCKS')
            print(len(stocks))
            schedule(stocks)
            break


if __name__ == '__main__':
    main()
