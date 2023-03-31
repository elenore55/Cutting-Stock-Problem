from math import floor, ceil
from copy import deepcopy
from random import randint, shuffle  # inclusive range

L = 10
l_arr = [4, 3, 2]
d_arr = [50, 30, 35]
S = sum([l_arr[i] * d_arr[i] for i in range(len(l_arr))])
N = 3
CHROMOSOME_LEN = 2 * N
POPULATION_SIZE = 15


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
    P = 1
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


if __name__ == '__main__':
    patterns = generate_efficient_patterns()
    max_repeat = calculate_max_pattern_repetition(patterns)
    initial_population = initialize_population(max_repeat)
    print(patterns)
    print(max_repeat)
    # print(initial_population)
    print(evaluate_fitness(initial_population[0], patterns))
