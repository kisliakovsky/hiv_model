import random

SYRINGE_INFECTION_GENERATOR = random.Random()
DRUG_USER_INFECTION_GENERATOR = random.Random()
BLEACH_RANDOM_GENERATOR = random.Random()
BLEACH_PROBABILITY = 0.37
SYRINGE_INFECTION_PROBABILITY = 0.18
DRUG_USER_INFECTION_PROBABILITY = 0.0105


class Syringe(object):

    def __init__(self):
        self.__is_infected = False

    @property
    def is_infected(self):
        return self.__is_infected

    def infect(self):
        self.__is_infected = True

    def use(self, user: 'DrugUser'):
        if user.is_infected:
            self.__is_infected = True

    def bleach(self):
        probability = BLEACH_RANDOM_GENERATOR.random()
        if probability <= BLEACH_PROBABILITY:
            self.__is_infected = False

    @staticmethod
    def get_clean_syringe():
        return Syringe()

    @staticmethod
    def get_infected_syringe():
        syringe = Syringe()
        syringe.infect()
        return syringe


class DrugUser(object):

    def __init__(self, is_infected=False):
        self.__is_infected = is_infected

    @property
    def is_infected(self):
        return self.__is_infected

    def infect(self):
        self.__is_infected = True

    def update(self):
        self.__is_infected = False

    def use_drug(self, syringe: Syringe):
        syringe.use(self)
        if syringe.is_infected:
            infection_probability = DRUG_USER_INFECTION_GENERATOR.random()
            if infection_probability < DRUG_USER_INFECTION_PROBABILITY:
                self.infect()
        else:
            infection_probability = SYRINGE_INFECTION_GENERATOR.random()
            if infection_probability < SYRINGE_INFECTION_PROBABILITY:
                syringe.infect()

    @staticmethod
    def get_clean_drug_user():
        return DrugUser()

    @staticmethod
    def get_infected_drug_user():
        return DrugUser(True)
