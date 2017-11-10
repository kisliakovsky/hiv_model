from random import Random
from typing import List, Tuple

from src.model.entity import Syringe, DrugUser, SyringeBag
from src.model.model import Model


class DiscreteTimeModel(Model):

    _NAME = "Discrete time model"

    POPULATION_GENERATOR_SEED = 47
    SCREENING_GENERATOR_SEED = 515701
    SHARING_GENERATOR_SEED = 570859

    PROBABILITY_TO_SAMPLE_INFECTED = 0.1
    SCREENING_PROBABILITY = 25 / 36500
    SHARING_PROBABILITY = 0.36

    def __init__(self, number_of_days: int, population_size: int, number_of_syringes: int):
        self.__number_of_days = number_of_days
        self.__population_size = population_size
        self.__population = self._generate_population(population_size)
        self.__bag_of_syringes = SyringeBag(number_of_syringes)
        self.__screening_generator = Random(DiscreteTimeModel.SCREENING_GENERATOR_SEED)
        self.__sharing_generator = Random(DiscreteTimeModel.SHARING_GENERATOR_SEED)

    @staticmethod
    def _generate_population(population_size) -> List[DrugUser]:
        population = []
        user_generator = Random(DiscreteTimeModel.POPULATION_GENERATOR_SEED)
        for i in range(population_size):
            is_infected = False
            if user_generator.random() <= DiscreteTimeModel.PROBABILITY_TO_SAMPLE_INFECTED:
                is_infected = True
            population.append(DrugUser(is_infected))
        return population

    def run(self) -> Tuple[List[float], List[float], List[float]]:
        timeline = []
        numbers_of_infected = []
        numbers_of_clean = []
        for i in range(self.__number_of_days):
            timeline.append(i)
            self.__perform_population_day()
            number_of_infected, number_of_clean = self.__count_infected_and_clean()
            numbers_of_infected.append(number_of_infected)
            numbers_of_clean.append(number_of_clean)
        return timeline, numbers_of_infected, numbers_of_clean

    def __perform_population_day(self):
        indices_of_quitting_infectious = []
        for i, drug_user in enumerate(self.__population):
                syringe = self.__bag_of_syringes.get_out_random_syringe()
                if self.__screening_generator.random() <= DiscreteTimeModel.SCREENING_PROBABILITY:
                    if drug_user.is_infected:
                        drug_user.update()
                        indices_of_quitting_infectious.append(i)
                    else:
                        continue
                else:
                    if self.__sharing_generator.random() <= DiscreteTimeModel.SHARING_PROBABILITY:
                        syringe.bleach()
                        drug_user.use_drug(syringe)
                    else:
                        continue

    def __count_infected_and_clean(self):
        number_of_infected = 0
        number_of_clean = 0
        for user in self.__population:
            if user.is_infected:
                number_of_infected += 1
            else:
                number_of_clean += 1
        return number_of_infected, number_of_clean

    def get_name(self) -> str:
        return self._NAME

    def get_population_size(self) -> int:
        return self.__population_size
