from copy import deepcopy
from random import shuffle, randint, choices, sample

MAX_ITERATIONS = 100
POPULATION_SIZE = 50
SIZE_CHANGED_COST = 7
STOCK_CHANGED_COST = 2


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
        if previous[1] != current[1]:
            cost += SIZE_CHANGED_COST
        elif previous[0] != current[0]:
            cost += STOCK_CHANGED_COST
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


def naive_scheduling(stocks):
    lengths = [4, 3, 2]
    i = 0
    cost = -STOCK_CHANGED_COST
    while True:
        length = lengths[i]
        for j, stock in enumerate(stocks):
            if length in stock:
                cost += STOCK_CHANGED_COST
        i += 1
        if i == len(lengths):
            break
        cost += SIZE_CHANGED_COST
    print(cost)
