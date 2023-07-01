from math import floor, ceil
from copy import deepcopy
from random import randint, shuffle, random, choice, choices
import matplotlib.pyplot as plt
from data_reader import DataReader
import time


class GA_Optimizer(object):

    def __init__(self, population_size=300, penalty=2, mutation_rate=0.1):
        self.MAX_ITERATIONS = 2000
        self.POPULATION_SIZE = population_size
        self.stock_length = None
        self.l_arr = []
        self.d_arr = []
        self.N = None
        self.penalty = penalty
        self.mutation_rate = mutation_rate

    def generate_efficient_patterns(self):
        result = []
        A_arr = [min(floor(self.stock_length / self.l_arr[0]), self.d_arr[0])]
        for n in range(1, self.N):
            s = sum([A_arr[j] * self.l_arr[j] for j in range(n)])
            A_arr.append(min(floor((self.stock_length - s) / self.l_arr[n]), self.d_arr[n]))

        while True:
            result.append(A_arr)
            for j in range(self.N - 2, -1, -1):
                if A_arr[j] > 0:
                    k = j
                    break
            else:
                return result

            A_arr_new = []
            for j in range(k):
                A_arr_new.append(A_arr[j])
            A_arr_new.append(A_arr[k] - 1)
            for n in range(k + 1, self.N):
                s = sum([A_arr_new[j] * self.l_arr[j] for j in range(n)])
                A_arr_new.append(min(floor((self.stock_length - s) / self.l_arr[n]), self.d_arr[n]))
            A_arr = deepcopy(A_arr_new)

    def calculate_max_pattern_repetition(self, patterns_arr):
        result = []
        for pattern in patterns_arr:
            max_rep = 0
            for i in range(len(pattern)):
                if pattern[i] > 0:
                    needed_rep = ceil(self.d_arr[i] / pattern[i])
                    if needed_rep > max_rep:
                        max_rep = needed_rep
            result.append(max_rep)
        return result

    def initialize_population(self, max_repeat_arr):
        init_population = []
        pairs = list(zip(range(len(max_repeat_arr)), max_repeat_arr))
        for i in range(self.POPULATION_SIZE):
            chromosome = []
            shuffle(pairs)
            for j in range(self.N):
                chromosome.append(pairs[j][0])
                chromosome.append(randint(1, pairs[j][1]))
            init_population.append(chromosome)
        return init_population

    def evaluate_fitness(self, chromosome, patterns_arr):
        P = self.penalty
        unsupplied_sum = 0
        l_provided = [0] * self.N
        for i in range(0, len(chromosome), 2):
            pattern = patterns_arr[chromosome[i]]
            for j in range(len(pattern)):
                l_provided[j] += pattern[j] * chromosome[i + 1]
        for i in range(self.N):
            num_unsupplied = self.d_arr[i] - l_provided[i]
            if num_unsupplied > 0:
                unsupplied_sum += num_unsupplied * self.l_arr[i]
        x_sum = self.stock_length * sum(chromosome[i] for i in range(1, len(chromosome), 2))
        S = sum([self.l_arr[i] * self.d_arr[i] for i in range(self.N)])
        return S / (x_sum + P * unsupplied_sum)

    @staticmethod
    def select_parents(fitness_pairs):
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

    @staticmethod
    def select_parents2(fitness_pairs):
        n = len(fitness_pairs)
        probabilities_sum = n * (n + 1) / 2
        probabilities = [i / probabilities_sum for i in range(n + 1, 1, -1)]
        return choices([pair[0] for pair in fitness_pairs], weights=probabilities, k=2)

    @staticmethod
    def crossover(parent1, parent2):
        n = len(parent1)
        point1_options = [i for i in range(2, n - 2, 2)]
        point1_index = choice(point1_options)
        point2_options = [i for i in range(point1_index + 2, n, 2)]
        point2_index = choice(point2_options)
        child1 = parent1[:point1_index] + parent2[point1_index: point2_index] + parent1[point2_index:]
        child2 = parent2[:point1_index] + parent1[point1_index: point2_index] + parent2[point2_index:]
        return child1, child2

    def mutate(self, chromosome, max_repeat_arr):
        # for now change repetition only
        for i in range(1, len(chromosome), 2):
            if random() < 1 / self.stock_length:
                repeat = max_repeat_arr[chromosome[i - 1]]
                chromosome[i] = randint(1, repeat)
        return chromosome

    def mutate2(self, chromosome, max_repeat_arr, patterns):
        for i in range(0, len(chromosome), 2):
            if random() < self.mutation_rate:
                new_pattern_index = randint(0, len(patterns) - 1)
                repeat = max_repeat_arr[new_pattern_index]
                chromosome[i] = new_pattern_index
                chromosome[i + 1] = randint(1, repeat)
        return chromosome

    def run(self, population, patterns_arr, max_repeat_arr, problem_path):
        start = time.time()
        best_results = []
        num_iters_same_result = 0
        last_result = float('inf')
        iter_cnt = self.MAX_ITERATIONS
        for count in range(self.MAX_ITERATIONS):
            if num_iters_same_result >= 100:
                iter_cnt = count
                break
            fitness_pairs = []
            for ch in population:
                fitness_pairs.append((ch, self.evaluate_fitness(ch, patterns_arr)))
            fitness_pairs.sort(key=lambda x: x[1], reverse=True)
            # Elitism 3
            next_generation = [fitness_pairs[0][0], fitness_pairs[1][0], fitness_pairs[2][0]]
            best_result_for_iter = fitness_pairs[0][1]
            if best_result_for_iter == 1:
                iter_cnt = count
                break

            best_results.append(best_result_for_iter)
            # sum_of_fitness = sum(fitness_pairs[i][1] for i in range(2, len(fitness_pairs)))
            # probabilities = [fitness_pairs[i][1] / sum_of_fitness for i in range(2, len(fitness_pairs))]

            if abs(best_result_for_iter - last_result) < 0.00001:
                num_iters_same_result += 1
            else:
                num_iters_same_result = 0
            last_result = best_result_for_iter

            for i in range(3, len(fitness_pairs), 2):
                parent1, parent2 = self.select_parents2(fitness_pairs)
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1, max_repeat_arr)
                child2 = self.mutate2(child2, max_repeat_arr, patterns_arr)
                next_generation.append(child1)
                next_generation.append(child2)
            population = deepcopy(next_generation)

        fitness_pairs = []
        for ch in population:
            fitness_pairs.append((ch, self.evaluate_fitness(ch, patterns_arr)))
        fitness_pairs.sort(key=lambda x: x[1], reverse=True)
        chosen_pattern = fitness_pairs[0][0]
        end_time = time.time()
        # print(fitness_pairs[0])
        # print(sum(chosen_pattern[i] for i in range(1, len(chosen_pattern), 2)))
        plt.plot(range(1, len(best_results) + 1), best_results)
        plt.xlabel('Iteration')
        plt.ylabel('Fitness')
        plt.show()
        stocks = []
        for i in range(0, len(chosen_pattern), 2):
            compact_pattern = patterns_arr[chosen_pattern[i]]
            actual_pattern = []
            for j in range(self.N):
                actual_pattern.extend([self.l_arr[j]] * compact_pattern[j])
            repeat = chosen_pattern[i + 1]
            for j in range(repeat):
                stocks.append(actual_pattern)
        # print(stocks)
        # with open('best_config_ga.csv', 'a') as file:
        #     file.write(
        #         f'{self.POPULATION_SIZE},{self.penalty},{self.mutation_rate},{problem_path},{len(stocks)},{fitness_pairs[0][1]},{iter_cnt},{end_time - start}\n')
        return stocks

    def optimize(self, problem_path, queue=None):
        self.stock_length, self.l_arr, self.d_arr = DataReader.read(problem_path)
        self.N = len(self.l_arr)
        patterns = self.generate_efficient_patterns()
        max_repeat = self.calculate_max_pattern_repetition(patterns)
        initial_population = self.initialize_population(max_repeat)
        stocks = self.run(initial_population, patterns, max_repeat, problem_path)
        if queue is not None:
            queue.put((self.stock_length, self.l_arr, self.d_arr, stocks))


if __name__ == '__main__':
    optimizer = GA_Optimizer()
    optimizer.optimize('data/problem10.txt')
