from random import random, choices
from math import sin, pi


class Solution:

    def __init__(self, constraints_min, constraints_max, params_amount=2, *params_vec):
        self.params_amount = params_amount
        self.constraints_min = constraints_min
        self.constraints_max = constraints_max
        self.params_vec = list(*params_vec) if params_vec else \
            [self.randomize(self.constraints_min, self.constraints_max) for x in range(self.params_amount)]
        self.fitness = fitness_function(*self.params_vec)

    def clone(self):
        return Solution(self.constraints_min, self.constraints_max, self.params_amount, self.params_vec)

    def crossover(self, parent2):
        result_params_vec = list()
        for idx, x in enumerate(self.params_vec):
            if random() > 0.5:
                result_params_vec.append(x)
            else:
                result_params_vec.append(parent2.params_vec[idx])

        return Solution(self.constraints_min, self.constraints_max, self.params_amount, result_params_vec)

    def mutate(self, probability=0.05):
        for idx, gene in enumerate(self.params_vec):
            if random() < probability:
                self.params_vec[idx] = random() * 3.14
        self.fitness = fitness_function(*self.params_vec)

    def __str__(self):
        result = f'Solution with fitness:{self.fitness}\n'
        result += f'Parametry to: {self.params_vec}\n'
        return result

    @staticmethod
    def randomize(constraints_min, constraints_max):
        return constraints_min + (random() * (constraints_max - constraints_min))


class EvolutionAlgorithm:
    # EvolutionAlgoritm(population_size, minimum_constraint, maximum_constraint, number_of_dimensions)

    def __init__(self, max_population_size, constraints_min, constraints_max, params_amount=2):
        self.population_vector = list()
        self.population_size = 0
        self.max_population_size = max_population_size
        self.constraints_min = constraints_min
        self.constraints_max = constraints_max
        self.params_amount = params_amount
        self.best_solution = None
        self.worst_solution = None
        self.mean_fit = 0

    def tournament_selection(self):
        parents = choices(self.population_vector, k=(self.max_population_size // 2))
        parents = sorted(parents, key=lambda agent: agent.fitness, reverse=True)
        return parents[0]

    def get_solution(self):

        if self.population_size < self.max_population_size:
            eval_s = Solution(self.constraints_min, self.constraints_max, params_amount=self.params_amount)
            self.population_vector.append(eval_s)
            self.population_size += 1
        else:
            # populacja jest pełna
            if random() > 0.5:  # tworzenie chromosonu przez krzyżowanie
                p1 = self.tournament_selection()
                p2 = self.tournament_selection()
                while p1 is p2:
                    p2 = self.tournament_selection()
                eval_s = p1.crossover(p2)
            else:  # tworzenie chromosonu przez klonowanie
                p1 = self.tournament_selection()
                eval_s = p1.clone()
            eval_s.mutate()
            self.feed_fitness(eval_s)

    def best_n_worst(self):
        best = self.best_solution if self.best_solution is not None else self.population_vector[0]
        worst = self.worst_solution if self.worst_solution is not None else self.population_vector[0]
        suma = 0
        for person in self.population_vector:  # znajdowanie najlepszego i najgorszego
            suma += person.fitness
            if worst.fitness > person.fitness:
                worst = person
            if best.fitness < person.fitness:
                best = person
        self.best_solution = best
        self.worst_solution = worst
        self.mean_fit = suma / self.max_population_size

    def feed_fitness(self, eval_s):
        self.best_n_worst()
        if eval_s.fitness > self.worst_solution.fitness:
            self.population_vector.remove(self.worst_solution)
            self.population_vector.append(eval_s)
            self.worst_solution = None
            self.best_n_worst()


def fitness_function(*args):
    value = michalewicz_x_d(*args)
    fitness = (-value)
    return fitness


def michalewicz_x_d(*arg):  # funkcja michalewicza dla dowolnej liczby wymiarów
    result = 0
    for idx, x in enumerate(arg, start=1):
        result -= sin(x) * sin(idx * x ** 2 / pi) ** 20
    return result


if __name__ == '__main__':
    # aktualnie klasa EvolutionAlgorithm obsługuje dowolną liczbę wymiarów
    # EvolutionAlgoritm(population_size, minimum_constraint, maximum_constraint, number_of_dimensions)
    ea = EvolutionAlgorithm(10, 0.0, 3.14, 2)

    for i in range(10000):
        ea.get_solution()
        print(ea.mean_fit)
        print(ea.best_solution)

    print(f'\nKoniec! najlepszy uzyskany wynik to: {ea.best_solution.fitness}')
    for idx, x in enumerate(ea.best_solution.params_vec):
        print(f'x{idx + 1} to: {x}')
