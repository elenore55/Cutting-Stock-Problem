from math import floor, ceil
from copy import deepcopy
from random import randint, shuffle, random, choice  # inclusive range
import matplotlib.pyplot as plt

# L = 10
# l_arr = [4, 3, 2]
# d_arr = [50, 30, 35]
# S = sum([l_arr[i] * d_arr[i] for i in range(len(l_arr))])
# N = 3
# CHROMOSOME_LEN = 2 * N

# L - big stock length
# N - broj malih stockova
POPULATION_SIZE = 300
MAX_ITERATIONS = 2000


def generate_efficient_patterns(stock_length, l_arr, d_arr):
    result = []
    N = len(l_arr)
    A_arr = [min(floor(stock_length / l_arr[0]), d_arr[0])]
    for n in range(1, N):
        s = sum([A_arr[j] * l_arr[j] for j in range(n)])
        A_arr.append(min(floor((stock_length - s) / l_arr[n]), d_arr[n]))

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
            A_arr_new.append(min(floor((stock_length - s) / l_arr[n]), d_arr[n]))
        A_arr = deepcopy(A_arr_new)


def calculate_max_pattern_repetition(patterns_arr, d_arr):
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


def initialize_population(max_repeat_arr, N):
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


def evaluate_fitness(chromosome, patterns_arr, l_arr, d_arr, stock_length):
    P = 2
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
    x_sum = stock_length * sum(chromosome[i] for i in range(1, len(chromosome), 2))
    S = sum([l_arr[i] * d_arr[i] for i in range(len(l_arr))])
    return S / (x_sum + P * unsupplied_sum)


def run(population, patterns_arr, max_repeat_arr, l_arr, d_arr, stock_length):
    best_results = []
    num_iters_same_result = 0
    last_result = float('inf')
    for count in range(MAX_ITERATIONS):
        if num_iters_same_result >= 100:
            break
        fitness_pairs = []
        for ch in population:
            fitness_pairs.append((ch, evaluate_fitness(ch, patterns_arr, l_arr, d_arr, stock_length)))
        fitness_pairs.sort(key=lambda x: x[1], reverse=True)
        # Elitism 3
        next_generation = [fitness_pairs[0][0], fitness_pairs[1][0], fitness_pairs[2][0]]
        best_result_for_iter = fitness_pairs[0][1]

        best_results.append(best_result_for_iter)
        # sum_of_fitness = sum(fitness_pairs[i][1] for i in range(2, len(fitness_pairs)))
        # probabilities = [fitness_pairs[i][1] / sum_of_fitness for i in range(2, len(fitness_pairs))]

        if abs(best_result_for_iter - last_result) < 0.00001:
            num_iters_same_result += 1
        else:
            num_iters_same_result = 0
        last_result = best_result_for_iter

        for i in range(3, len(fitness_pairs), 2):
            parent1, parent2 = choose_parents(fitness_pairs)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, max_repeat_arr, stock_length)
            child2 = mutate2(child2, max_repeat_arr, stock_length, patterns_arr)
            next_generation.append(child1)
            next_generation.append(child2)
        population = deepcopy(next_generation)

    fitness_pairs = []
    for ch in population:
        fitness_pairs.append((ch, evaluate_fitness(ch, patterns_arr, l_arr, d_arr, stock_length)))
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
    plt.plot(range(1, len(best_results) + 1), best_results)
    plt.xlabel('Iteration')
    plt.ylabel('Best result')
    plt.show()


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


def mutate(chromosome, max_repeat_arr, stock_length):
    # for now change repetition only
    for i in range(1, len(chromosome), 2):
        if random() < 1 / stock_length:
            repeat = max_repeat_arr[chromosome[i - 1]]
            chromosome[i] = randint(1, repeat)
    return chromosome


def mutate2(chromosome, max_repeat_arr, stock_length, patterns):
    for i in range(0, len(chromosome), 2):
        if random() < 0.1:
            new_pattern_index = randint(0, len(patterns) - 1)
            repeat = max_repeat_arr[new_pattern_index]
            chromosome[i] = new_pattern_index
            chromosome[i + 1] = randint(1, repeat)
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


def read_data(file_name):
    path = 'data/' + file_name
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


def optimize():
    stock_length, l_arr, d_arr = read_data('problem2.txt')
    patterns = generate_efficient_patterns(stock_length, l_arr, d_arr)
    max_repeat = calculate_max_pattern_repetition(patterns, d_arr)
    initial_population = initialize_population(max_repeat, len(l_arr))
    # print(patterns)
    run(initial_population, patterns, max_repeat, l_arr, d_arr, stock_length)


if __name__ == '__main__':
    optimize()
