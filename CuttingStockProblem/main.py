from math import floor, ceil
from copy import deepcopy
from random import randint, shuffle, random, choice  # inclusive range

L = 10
l_arr = [4, 3, 2]
d_arr = [50, 30, 35]
S = sum([l_arr[i] * d_arr[i] for i in range(len(l_arr))])
N = 3
CHROMOSOME_LEN = 2 * N
POPULATION_SIZE = 50
MAX_ITERATIONS = 1000


def generate_efficient_patterns():
    result = []

    A_arr = [min(floor(L / l_arr[0]), d_arr[0])]
    for n in range(1, N):
        s = sum([A_arr[j] * l_arr[j] for j in range(n)])
        A_arr.append(min(floor((L - s) / l_arr[n]), d_arr[n]))

    while True:
        result.append(A_arr)

        for j in range(N - 2, -1, -1):
            if A_arr[j] > 0:
                k = j
                break
        else:
            return result

        A_arr_new = []
        for j in range(k):
            A_arr_new.append(A_arr[j])
        A_arr_new.append(A_arr[k] - 1)
        for n in range(k + 1, N):
            s = sum([A_arr_new[j] * l_arr[j] for j in range(n)])
            A_arr_new.append(min(floor((L - s) / l_arr[n]), d_arr[n]))
        A_arr = deepcopy(A_arr_new)


def calculate_max_pattern_repetition(patterns_arr):
    result = []
    for pattern in patterns_arr:
        max_rep = 0
        for i in range(len(pattern)):
            if pattern[i] > 0:
                needed_rep = ceil(d_arr[i] / pattern[i])
                if needed_rep > max_rep:
                    max_rep = needed_rep
        result.append(max_rep)
    return result


def initialize_population(max_repeat_arr):
    init_population = []
    pairs = list(zip(range(len(max_repeat_arr)), max_repeat_arr))
    for i in range(POPULATION_SIZE):
        chromosome = []
        shuffle(pairs)
        for j in range(N):
            chromosome.append(pairs[j][0])
            chromosome.append(randint(1, pairs[j][1]))
        init_population.append(chromosome)
    return init_population


def evaluate_fitness(chromosome, patterns_arr):
    P = 10
    unsupplied_sum = 0
    l_provided = [0] * len(l_arr)
    for i in range(0, len(chromosome), 2):
        pattern = patterns_arr[chromosome[i]]
        for j in range(len(pattern)):
            l_provided[j] += pattern[j] * chromosome[i + 1]
    for i in range(len(l_arr)):
        num_unsupplied = d_arr[i] - l_provided[i]
        if num_unsupplied > 0:
            unsupplied_sum += num_unsupplied * l_arr[i]
    x_sum = L * sum(chromosome[i] for i in range(1, len(chromosome), 2))
    return S / (x_sum + P * unsupplied_sum)


def run(population, patterns_arr, max_repeat_arr):
    for count in range(MAX_ITERATIONS):
        fitness_pairs = []
        for ch in population:
            fitness_pairs.append((ch, evaluate_fitness(ch, patterns_arr)))
        fitness_pairs.sort(key=lambda x: x[1], reverse=True)
        next_generation = [fitness_pairs[0][0], fitness_pairs[1][0]]
        # sum_of_fitness = sum(fitness_pairs[i][1] for i in range(2, len(fitness_pairs)))
        # probabilities = [fitness_pairs[i][1] / sum_of_fitness for i in range(2, len(fitness_pairs))]

        for i in range(2, len(fitness_pairs), 2):
            parent1, parent2 = choose_parents(fitness_pairs)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, max_repeat_arr)
            child2 = mutate(child2, max_repeat_arr)
            next_generation.append(child1)
            next_generation.append(child2)
        population = deepcopy(next_generation)

    fitness_pairs = []
    for ch in population:
        fitness_pairs.append((ch, evaluate_fitness(ch, patterns_arr)))
    fitness_pairs.sort(key=lambda x: x[1], reverse=True)
    chosen_pattern = fitness_pairs[0][0]
    l_final = [0] * len(l_arr)
    for i in range(0, len(chosen_pattern), 2):
        p = patterns_arr[i]
        for j in range(len(p)):
            l_final[j] += chosen_pattern[i + 1] * p[j]
    print(fitness_pairs[0])
    print(l_final)
    print(sum(chosen_pattern[i] for i in range(1, len(chosen_pattern), 2)))


def choose_parents(fitness_pairs):
    n = len(fitness_pairs)
    max_val1 = max_val2 = float('-inf')
    index1 = index2 = None
    for i in range(n):
        score = (n - i) * random()
        if score > max_val1:
            max_val1, max_val2 = score, max_val1
            index1, index2 = i, index1
        elif score > max_val2:
            max_val2 = score
            index2 = i
    return fitness_pairs[index1][0], fitness_pairs[index2][0]


def mutate(chromosome, max_repeat_arr):
    # for now change repetition only
    for i in range(1, len(chromosome), 2):
        if random() > 1 / L:
            repeat = max_repeat_arr[chromosome[i - 1]]
            chromosome[i] = randint(1, repeat)
    return chromosome


def crossover(parent1, parent2):
    n = len(parent1)
    point1_options = [i for i in range(2, n - 2, 2)]
    point1_index = choice(point1_options)
    point2_options = [i for i in range(point1_index + 2, n, 2)]
    point2_index = choice(point2_options)
    child1 = parent1[:point1_index] + parent2[point1_index: point2_index] + parent1[point2_index:]
    child2 = parent2[:point1_index] + parent1[point1_index: point2_index] + parent2[point2_index:]
    return child1, child2


if __name__ == '__main__':
    patterns = generate_efficient_patterns()
    max_repeat = calculate_max_pattern_repetition(patterns)
    initial_population = initialize_population(max_repeat)
    print(patterns)
    run(initial_population, patterns, max_repeat)
