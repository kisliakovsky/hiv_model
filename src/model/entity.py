from random import Random

SYRINGE_INFECTION_GENERATOR_SEED = 496231
DRUG_USER_INFECTION_GENERATOR_SEED = 952207
BLEACH_RANDOM_GENERATOR_SEED = 852199

SYRINGE_INFECTION_GENERATOR = Random(SYRINGE_INFECTION_GENERATOR_SEED)
DRUG_USER_INFECTION_GENERATOR = Random(DRUG_USER_INFECTION_GENERATOR_SEED)
BLEACH_RANDOM_GENERATOR = Random(BLEACH_RANDOM_GENERATOR_SEED)
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
        if BLEACH_RANDOM_GENERATOR.random() <= BLEACH_PROBABILITY:
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
            if DRUG_USER_INFECTION_GENERATOR.random() < DRUG_USER_INFECTION_PROBABILITY:
                self.infect()
        else:
            if SYRINGE_INFECTION_GENERATOR.random() < SYRINGE_INFECTION_PROBABILITY:
                syringe.infect()

    @staticmethod
    def get_clean_drug_user():
        return DrugUser()

    @staticmethod
    def get_infected_drug_user():
        return DrugUser(True)


class SyringeBag(object):

    SYRINGE_RANDOMIZER_SEED = 1337

    def __init__(self, number_of_syringes):
        self.__syringes = [Syringe() for _ in range(number_of_syringes)]
        self.__extraction_generator = Random(SyringeBag.SYRINGE_RANDOMIZER_SEED)

    def get_out_random_syringe(self):
        index = self.__extraction_generator.randint(0, len(self.__syringes) - 1)
        return self.__syringes[index]
