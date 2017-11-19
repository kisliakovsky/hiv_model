from typing import Tuple, List
from random import Random

from src.model.model import Model


class ContinuousTimeModel(Model):

    _NAME = "Continuous time model"

    POPULATION_GENERATOR_SEED = 47
    GENERATOR_SEED = 531521

    PROBABILITY_TO_SAMPLE_INFECTED = 0.1
    SCREENING_RATE = 14.97 / 365 / 100
    INJECTION_RATE = 1.21
    SHARING_PROBABILITY = 0.36
    SYRINGE_INFECTION_PROBABILITY = 0.18
    NOT_SYRINGE_INFECTION_PROBABILITY = 1 - SYRINGE_INFECTION_PROBABILITY
    DRUG_USER_INFECTION_PROBABILITY = 0.0105
    NOT_DRUG_USER_INFECTION_PROBABILITY = 1 - DRUG_USER_INFECTION_PROBABILITY
    BLEACH_PROBABILITY = 0.37
    NOT_BLEACH_PROBABILITY = 1 - BLEACH_PROBABILITY

    def __init__(self, number_of_days: int, population_size: int, number_of_syringes: int):
        self.__number_of_days = number_of_days
        self.__population_size = population_size
        self.__number_of_syringes = number_of_syringes
        self.__number_of_infected_users = self._infect_population(population_size)
        self.__number_of_infected_syringes = 0
        self.__event_generator = Random(ContinuousTimeModel.GENERATOR_SEED)

    @staticmethod
    def _infect_population(population_size) -> int:
        user_generator = Random(ContinuousTimeModel.POPULATION_GENERATOR_SEED)
        number_of_infected = 0
        for i in range(population_size):
            if user_generator.random() < ContinuousTimeModel.PROBABILITY_TO_SAMPLE_INFECTED:
                number_of_infected += 1
        return number_of_infected

    def run(self) -> Tuple[List[float], List[float], List[float]]:
        t = 0
        timeline = [t]
        numbers_of_infected = [self.get_number_of_infected_users()]
        numbers_of_clean = [self.get_number_of_clean_users()]
        rates_calculators = [self.__calculate_rate_1, self.__calculate_rate_2, self.__calculate_rate_3, self.__calculate_rate_4]
        outcomes = [self.__perform_outcome_1, self.__perform_outcome_2, self.__perform_outcome_3, self.__perform_outcome_4]
        while t < 10000:
            delta_times = []
            for index, rates_calculator in enumerate(rates_calculators):
                rate = rates_calculator()
                if rate == 0:
                    rate = 0.0000000001
                delta_time = self.__event_generator.expovariate(rate)
                delta_times.append(delta_time)
            min_delta_time = min(delta_times)
            outcome_index = delta_times.index(min_delta_time)
            outcomes[outcome_index]()
            t += min_delta_time
            timeline.append(t)
            numbers_of_infected.append(self.get_number_of_infected_users())
            numbers_of_clean.append(self.get_number_of_clean_users())
        return timeline, numbers_of_infected, numbers_of_clean

    def __calculate_rate_1(self):
        return self.get_number_of_infected_users() * ContinuousTimeModel.SCREENING_RATE

    def __calculate_rate_2(self):
        prerate = self.__calculate_prerate()
        return prerate * self.__calculate_probability_of_state_1() * ContinuousTimeModel.SYRINGE_INFECTION_PROBABILITY

    def __calculate_rate_3(self):
        prerate = self.__calculate_prerate()
        return prerate * ContinuousTimeModel.BLEACH_PROBABILITY * (self.__calculate_probability_of_state_2() * ContinuousTimeModel.NOT_SYRINGE_INFECTION_PROBABILITY + self.__calculate_probability_of_state_4())

    def __calculate_rate_4(self):
        prerate = self.__calculate_prerate()
        return prerate * ContinuousTimeModel.NOT_BLEACH_PROBABILITY * self.__calculate_probability_of_state_4() * ContinuousTimeModel.DRUG_USER_INFECTION_PROBABILITY

    def __calculate_prerate(self):
        return self.get_population_size() * ContinuousTimeModel.INJECTION_RATE * ContinuousTimeModel.SHARING_PROBABILITY

    def __calculate_probability_of_user_infected(self):
        return self.get_number_of_infected_users() / self.get_population_size()

    def __calculate_probability_of_user_not_infected(self):
        return 1 - self.__calculate_probability_of_user_infected()

    def __calculate_probability_of_syringe_infected(self):
        return self.get_number_of_infected_syringes() / self.get_number_of_syringes()

    def __calculate_probability_of_syringe_not_infected(self):
        return 1 - self.__calculate_probability_of_syringe_infected()

    def __calculate_probability_of_state_1(self):
        return self.__calculate_probability_of_user_infected() * self.__calculate_probability_of_syringe_not_infected()

    def __calculate_probability_of_state_2(self):
        return self.__calculate_probability_of_user_infected() * self.__calculate_probability_of_syringe_infected()

    def __calculate_probability_of_state_4(self):
        return self.__calculate_probability_of_user_not_infected() * self.__calculate_probability_of_syringe_infected()

    def __perform_outcome_1(self):
        self.__decrement_number_of_infected_users()

    def __perform_outcome_2(self):
        self.__increment_number_of_infected_syringes()

    def __perform_outcome_3(self):
        self.__decrement_number_of_infected_syringes()

    def __perform_outcome_4(self):
        self.__increment_number_of_infected_users()
        self.__decrement_number_of_infected_syringes()

    def __increment_number_of_infected_users(self):
        self.__number_of_infected_users += 1

    def __decrement_number_of_infected_users(self):
        if self.get_number_of_infected_users() > 0:
            self.__number_of_infected_users -= 1

    def __increment_number_of_infected_syringes(self):
        self.__number_of_infected_syringes += 1

    def __decrement_number_of_infected_syringes(self):
        if self.get_number_of_infected_syringes() > 0:
            self.__number_of_infected_syringes -= 1

    def get_number_of_infected_users(self):
        return self.__number_of_infected_users

    def get_number_of_clean_users(self):
        return self.get_population_size() - self.get_number_of_infected_users()

    def get_number_of_infected_syringes(self):
        return self.__number_of_infected_syringes

    def get_number_of_clean_syringes(self):
        return self.get_number_of_syringes() - self.get_number_of_infected_syringes()

    def get_name(self) -> str:
        return self._NAME

    def get_population_size(self) -> int:
        return self.__population_size

    def get_number_of_syringes(self) -> int:
        return self.__number_of_syringes
