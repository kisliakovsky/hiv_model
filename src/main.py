import math
import random

import numpy

from src import exporting
from src.model.continuous_time_model import ContinuousTimeModel
from src.model.discrete_time_model import DiscreteTimeModel


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

NUMBER_OF_DAYS = 10000
POPULATION_SIZE = 300
NUMBER_OF_SYRINGES = 10


def main():
    model1 = DiscreteTimeModel(NUMBER_OF_DAYS, POPULATION_SIZE, NUMBER_OF_SYRINGES)
    model2 = ContinuousTimeModel(NUMBER_OF_DAYS, POPULATION_SIZE, NUMBER_OF_SYRINGES)
    exporting.save_comparison(model1, model2, "HIV spread")


if __name__ == "__main__":
    main()
