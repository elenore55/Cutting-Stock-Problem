from random import shuffle
from copy import deepcopy

L = 10
l_arr = [4, 3, 2]
d_arr = [5, 3, 3]


def generate_initial_population(num_chromosomes, demand):
    population = []
    for _ in range(num_chromosomes):
        shuffle(demand)
        population.append(deepcopy(demand))
    return population


def main():
    demand = []
    for i in range(len(l_arr)):
        demand.extend([l_arr[i]] * d_arr[i])
    population = generate_initial_population(10, demand)
    print(population)


if __name__ == '__main__':
    main()
