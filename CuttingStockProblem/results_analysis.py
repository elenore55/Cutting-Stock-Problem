import EP_approach
import GA_approach

PROBLEMS = [f'data/problem{i}.txt' for i in range(1, 11)]
NUM_RUNS = 5
SOLUTIONS = {
    '1': 9,
    '2': 23,
    '3': 15,
    '4': 19,
    '5': 53,
    '6': 81,
    '7': 68,
    '8': 148,
    '9': 154,
    '10': 223,
    '0': 223
}


class Config(object):
    def __init__(self, value):
        self.value = value
        self.time_sum = 0
        self.error_sum = 0
        self.repeat = 0

    def get_avg_time(self):
        return self.time_sum / self.repeat

    def get_avg_error(self):
        return self.error_sum / self.repeat

    def __str__(self):
        return f'{self.repeat}'


class Result(object):
    def __init__(self, problem, best_fitness):
        self.problem = problem
        self.time_sum = 0
        self.repeat = 0
        self.fitness_sum = 0
        self.num_stocks_sum = 0
        self.best_result = float('inf')
        self.best_fitness = best_fitness
        self.iter_cnt_sum = 0

    def get_avg_time(self):
        return self.time_sum / self.repeat

    def get_avg_fitness(self):
        return self.fitness_sum / self.repeat

    def get_avg_num_stocks(self):
        return self.num_stocks_sum / self.repeat

    def get_avg_iter_cnt(self):
        return self.iter_cnt_sum / self.repeat


def run_for_ep():
    tournament_sizes = [5, 10, 20]
    num_3ps = [1, 2, 3]
    population_sizes = [50, 100, 200]
    gene_choice_modes = ['random', 'heuristic']
    for problem in PROBLEMS:
        for i in range(NUM_RUNS):
            print(f'{problem} - iteration {i} running...')
            for q in tournament_sizes:
                for num in num_3ps:
                    for size in population_sizes:
                        for mode in gene_choice_modes:
                            optimizer = EP_approach.EP_Optimizer(q=q, num_3ps=num, population_size=size, gene_choice=mode)
                            optimizer.optimize(problem)


def run_for_ga():
    population_sizes = [100, 200, 300]
    penalties = [1, 2, 3]
    mutation_rates = [0.05, 0.1, 0.15]
    for problem in PROBLEMS:
        for i in range(NUM_RUNS):
            print(f'{problem} - iteration {i} running...')
            for size in population_sizes:
                for p in penalties:
                    for rate in mutation_rates:
                        optimizer = GA_approach.GA_Optimizer(population_size=size, penalty=p, mutation_rate=rate)
                        optimizer.optimize(problem)


def get_best_config_ep():
    configs = {}
    with open('ep_results.csv') as file:
        for line in file.readlines():
            tokens = line.split(',')
            value = f'{tokens[0]},{tokens[1]},{tokens[2]},{tokens[3]}'
            if value not in configs:
                configs[value] = Config(value)
            problem = tokens[4][-5]
            config = configs[value]
            config.repeat += 1
            config.time_sum += float(tokens[-1])
            config.error_sum += abs(int(tokens[5]) - SOLUTIONS[problem])
    configs_list = list(configs.values())
    configs_list.sort(key=lambda x: (x.get_avg_error(), x.get_avg_time()))
    for c in configs_list:
        print(f'{c.value} {c.get_avg_error()} {c.get_avg_time()}')


def get_best_config_ga():
    configs = {}
    with open('ga_results.csv') as file:
        for line in file.readlines():
            tokens = line.split(',')
            value = f'{tokens[0]},{tokens[1]},{tokens[2]}'
            if value not in configs:
                configs[value] = Config(value)
            problem = tokens[3][-5]
            config = configs[value]
            config.repeat += 1
            config.time_sum += float(tokens[-1])
            config.error_sum += abs(int(tokens[4]) - SOLUTIONS[problem])
    configs_list = list(configs.values())
    configs_list.sort(key=lambda x: (x.get_avg_error(), x.get_avg_time()))
    for c in configs_list:
        print(f'{c.value} {c.get_avg_error()} {c.get_avg_time()}')


def run_best_config_ep():
    q = 15
    num_3ps = 2
    population_size = 100
    mode = 'heuristic'
    optimizer = EP_approach.EP_Optimizer(q, num_3ps, population_size, mode)
    for problem in PROBLEMS:
        print(f'Running for {problem}')
        for i in range(10):
            print(f'\tIteration {i + 1}')
            optimizer.optimize(problem)


def run_best_config_ga():
    mutation_rate = 0.15
    penalty = 2
    population_size = 300
    optimizer = GA_approach.GA_Optimizer(population_size, penalty, mutation_rate)
    for problem in PROBLEMS:
        print(f'Running for {problem}')
        for i in range(10):
            print(f'\tIteration {i + 1}')
            optimizer.optimize(problem)


def evaluate_results_ep():
    problems = {}
    with open('best_config_ep2.csv') as file:
        for line in file.readlines():
            tokens = line.split(',')
            problem = tokens[4][-5]
            if problem not in problems:
                problems[problem] = Result(problem, float('inf'))
            res = problems[problem]
            res.repeat += 1
            res.time_sum += float(tokens[-1])

            fitness = float(tokens[6])
            res.fitness_sum += fitness
            if fitness < res.best_fitness:
                res.best_fitness = fitness

            num_stocks = int(tokens[5])
            res.num_stocks_sum += num_stocks
            if num_stocks < res.best_result:
                res.best_result = num_stocks

            res.iter_cnt_sum += int(tokens[-2])

            problems[problem] = res
    for p in problems.values():
        print(f'{p.problem}: Best result: {p.best_result}, Best fitness: {p.best_fitness}, Average result: {p.get_avg_num_stocks()}, '
              f'Average fitness: {p.get_avg_fitness()}, Average time: {p.get_avg_time()}, Average iters: {p.get_avg_iter_cnt()}')

def evaluate_results_ga():
    problems = {}
    with open('best_config_ga.csv') as file:
        for line in file.readlines():
            tokens = line.split(',')
            problem = tokens[3][-5]
            if problem not in problems:
                problems[problem] = Result(problem, float('-inf'))
            res = problems[problem]
            res.repeat += 1
            res.time_sum += float(tokens[-1])

            fitness = float(tokens[5])
            res.fitness_sum += fitness
            if fitness > res.best_fitness:
                res.best_fitness = fitness

            num_stocks = int(tokens[4])
            res.num_stocks_sum += num_stocks
            if SOLUTIONS[problem] <= num_stocks < res.best_result:
                res.best_result = num_stocks

            res.iter_cnt_sum += int(tokens[-2])

            problems[problem] = res
    for p in problems.values():
        print(f'{p.problem}: Best result: {p.best_result}, Best fitness: {p.best_fitness}, Average result: {p.get_avg_num_stocks()}, '
              f'Average fitness: {p.get_avg_fitness()}, Average time: {p.get_avg_time()}, Average iters: {p.get_avg_iter_cnt()}')

if __name__ == '__main__':
    # run_for_ep()
    # run_for_ga()
    # get_best_config_ep()
    # get_best_config_ga()
    # run_best_config_ep()
    # run_best_config_ga()
    evaluate_results_ep()
