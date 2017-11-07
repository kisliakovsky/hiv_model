from typing import Tuple
from unittest import TestCase
from src.entity import DrugUser, Syringe


def perform_drug_usage(user_infection: bool, syringe_infection: bool) -> Tuple[DrugUser, Syringe]:
    user = DrugUser(user_infection)
    syringe = Syringe()
    if syringe_infection:
        syringe.infect()
    user.use_drug(syringe)
    return user, syringe


# noinspection PyPep8Naming
class TestEntityInteraction(TestCase):

    def testUserWillGetInfectedFromInfectedSyringeSometime(self):
        results = []
        for _ in range(100):
            user, syringe = perform_drug_usage(False, True)
            results.append(user.is_infected)
        self.assertTrue(any(results))

    def testSyringeWillGetInfectedFromInfectedUser(self):
        user, syringe = perform_drug_usage(True, False)
        self.assertTrue(syringe.is_infected)

    def testSyringeWillNotGetInfectedFromCleanUser(self):
        user, syringe = perform_drug_usage(False, False)
        self.assertFalse(syringe.is_infected)

    def testUserWillNotGetInfectedFromCleanSyringe(self):
        user, syringe = perform_drug_usage(False, False)
        self.assertFalse(user.is_infected)

    def testUserCannotBecomeUninfectedWithCleanSyringe(self):
        user, syringe = perform_drug_usage(True, False)
        self.assertTrue(user.is_infected)

    def testSyringeCannotBecomeUninfectedWithCleanUser(self):
        user, syringe = perform_drug_usage(False, True)
        self.assertTrue(syringe.is_infected)
