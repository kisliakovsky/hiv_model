from typing import Tuple, List
from random import Random
import numpy
from src.model.entity import SyringeBag

from src.model.model import Model


class ContinuousTimeModel(Model):

    _NAME = "Continuous time model"

    POPULATION_GENERATOR_SEED = 47
    SCREENING_GENERATOR_SEED = 531521
    SHARING_GENERATOR_SEED = 941753
    BLEACH_GENERATOR_SEED = 800993

    PROBABILITY_TO_SAMPLE_INFECTED = 0.1
    SCREENING_RATE = 14.97 / 365 / 100
    SHARING_RATE = 1.21
    BLEACH_RATE = 0.14
    NUMBER_OF_DELTAS = 1000000

    def __init__(self, number_of_days: int, population_size: int, number_of_syringes: int):
        self.__number_of_days = number_of_days
        self.__population_size = population_size
        self.__number_of_infected_users, self.__number_of_clean_users = self._divide_population(population_size)
        self.__number_of_infected_syringes, self.__number_of_clean_syringes = 0, number_of_syringes
        self.__screening_generator = Random(ContinuousTimeModel.SCREENING_GENERATOR_SEED)
        self.__sharing_generator = Random(ContinuousTimeModel.SHARING_GENERATOR_SEED)

    @staticmethod
    def _divide_population(population_size) -> Tuple[int, int]:
        user_generator = Random(ContinuousTimeModel.POPULATION_GENERATOR_SEED)
        number_of_clean = 0
        number_of_infected = 0
        for i in range(population_size):
            if user_generator.random() < ContinuousTimeModel.PROBABILITY_TO_SAMPLE_INFECTED:
                number_of_infected += 1
            else:
                number_of_clean += 1
        return number_of_infected, number_of_clean

    def run(self) -> Tuple[List[float], List[float], List[float]]:
        timeline = [0]
        size = len(timeline)
        number_of_infected_users = []
        number_of_clean_users = []
        for i in range(size):
            number_of_infected_users.append(50)
            number_of_clean_users.append(50)
        return timeline, number_of_infected_users, number_of_clean_users

    def get_name(self) -> str:
        return self._NAME

    def get_population_size(self) -> int:
        return self.__population_size
