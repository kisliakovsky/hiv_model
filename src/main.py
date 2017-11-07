import random
import math
from typing import List

import numpy

from src import exporting
from src.entity import DrugUser, Syringe

NUMBER_OF_DAYS = 10000
POPULATION_SIZE = 100
NUMBER_OF_SYRINGES = 20

SCREENING_PROBABILITY = 25 / 36500
SHARING_PROBABILITY = 0.36


def generate_population() -> List[DrugUser]:
    population = []
    random_generator = random.Random(47)
    for i in range(POPULATION_SIZE):
        infection_probability = random_generator.random()
        is_infected = False
        if infection_probability <= 0.1:
            is_infected = True
        population.append(DrugUser(is_infected))
    return population


def get_number_of_infectious(population: List[DrugUser]):
    number_of_infected = 0
    number_of_clean = 0
    for user in population:
        if user.is_infected:
            number_of_infected += 1
        else:
            number_of_clean += 1
    return number_of_infected, number_of_clean


syringe_generator = random.Random(1337)
screening_generator = random.Random()
sharing_generator = random.Random()
bleach_generator = random.Random()


def perform_population_day(population: List[DrugUser], syringes: List[Syringe]):
    indices_of_quitting_infectious = []
    for i, drug_user in enumerate(population):
            j = syringe_generator.randint(0, len(syringes) - 1)
            syringe = syringes[j]
            screening_probability = screening_generator.random()
            if screening_probability <= SCREENING_PROBABILITY:
                if drug_user.is_infected:
                    drug_user.update()
                    indices_of_quitting_infectious.append(i)
                else:
                    continue
            else:
                sharing_probability = sharing_generator.random()
                if sharing_probability <= SHARING_PROBABILITY:
                    syringe.bleach()
                    drug_user.use_drug(syringe)
                else:
                    continue
    return get_number_of_infectious(population)


def run_first_model():
    population = generate_population()
    syringes = [Syringe() for _ in range(10)]
    numbers_of_infected = []
    numbers_of_clean = []
    for _ in range(NUMBER_OF_DAYS):
        number_of_infected, number_of_clean = perform_population_day(population, syringes)
        numbers_of_infected.append(number_of_infected)
        numbers_of_clean.append(number_of_clean)
    exporting.save_stacked_plot(range(NUMBER_OF_DAYS), numbers_of_infected, numbers_of_clean,
                                "infection dynamics")


NUMBER_OF_POTENTIAL_IMMIGRANTS = 300
RATE_OF_IMMIGRATION = 0.5 * NUMBER_OF_POTENTIAL_IMMIGRANTS
generator = random.Random()


def run_temp_solution():
    t = 0
    n = 0
    xs = [t]
    ys = [NUMBER_OF_POTENTIAL_IMMIGRANTS]
    while t < 100:
        r = generator.random()
        theta = -1 / RATE_OF_IMMIGRATION * math.log(r)
        t += theta
        n += 1
        xs.append(t)
        ys.append(NUMBER_OF_POTENTIAL_IMMIGRANTS - n)
    exporting.save_plot(xs, ys, "immigration dynamics")


SCALE_OF_IMMIGRATION = 1 / 0.5
numpy.random.seed(47)
immigration_times = numpy.random.exponential(SCALE_OF_IMMIGRATION, 1000).tolist()


def main():
    t = 0
    number_of_actual_immigrants = 0
    xs = [t]
    ys = [NUMBER_OF_POTENTIAL_IMMIGRANTS]
    for delta_time in immigration_times:
        t += delta_time
        number_of_actual_immigrants += 1
        number_of_potential_immigrants = NUMBER_OF_POTENTIAL_IMMIGRANTS - number_of_actual_immigrants
        xs.append(t)
        ys.append(number_of_potential_immigrants)
    exporting.save_plot(xs, ys, "immigration dynamics")

if __name__ == "__main__":
    main()
