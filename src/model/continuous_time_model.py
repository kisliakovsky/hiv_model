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
    SCREENING_RATE = 1.0 / 36500
    SHARING_RATE = 1.21
    BLEACH_RATE = 0.14
    SCREENING_SCALE = 1.0 / SCREENING_RATE
    SHARING_RATE = 1.0 / SHARING_RATE
    BLEACH_SCALE = 1.0 / BLEACH_RATE
    NUMBER_OF_DELTAS = 1000000

    def __init__(self, number_of_days: int, population_size: int, number_of_syringes: int):
        self.__number_of_days = number_of_days
        self.__population_size = population_size
        self.__number_of_infected_users, self.__number_of_clean_users = self._divide_population(population_size)
        self.__number_of_infected_syringes, self.__number_of_clean_syringes = 0, number_of_syringes
        screening_times = ContinuousTimeModel._generate_times(ContinuousTimeModel.SCREENING_GENERATOR_SEED, ContinuousTimeModel.SCREENING_SCALE, ContinuousTimeModel.NUMBER_OF_DELTAS, 0)
        sharing_times = ContinuousTimeModel._generate_times(ContinuousTimeModel.SHARING_GENERATOR_SEED, ContinuousTimeModel.SHARING_RATE, ContinuousTimeModel.NUMBER_OF_DELTAS, 1)
        bleach_times = ContinuousTimeModel._generate_times(ContinuousTimeModel.BLEACH_GENERATOR_SEED, ContinuousTimeModel.BLEACH_SCALE, ContinuousTimeModel.NUMBER_OF_DELTAS, 2)
        times_list = [screening_times, sharing_times, bleach_times]
        self.__timeline = ContinuousTimeModel._times_to_timeline(times_list)


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

    @staticmethod
    def _generate_times(seed, scale, number_of_deltas, index):
        numpy.random.seed(seed)
        deltas = numpy.random.exponential(scale, number_of_deltas)
        return ContinuousTimeModel._deltas_to_times(deltas, index)

    @staticmethod
    def _times_to_timeline(times_list):
        all_times = []
        for times in times_list:
            all_times += times
        return sorted(all_times, key=lambda time: time[1])

    @staticmethod
    def _deltas_to_times(deltas, index):
        time = 0
        times = []
        for delta in deltas:
            time += delta
            times += ((index, time))
        return times



    def run(self) -> Tuple[List[float], List[float], List[float]]:
        size = len(self.__timeline)
        number_of_infected_users = []
        number_of_clean_users = []
        for i in range(size):
            number_of_infected_users.append(50)
            number_of_clean_users.append(50)
        return self.__timeline, number_of_infected_users, number_of_clean_users

    def get_name(self) -> str:
        return self._NAME

    def get_population_size(self) -> int:
        return self.__population_size
