from typing import Tuple, List

from src.model.model import Model


class ContinuousTimeModel(Model):

    _NAME = "Continuous time model"

    def __init__(self, number_of_days: int, population_size: int, number_of_syringes: int):
        self.__number_of_days = number_of_days
        self.__population_size = population_size

    def run(self) -> Tuple[List[float], List[float], List[float]]:
        return [0.0], [0.0], [0.0]

    def get_name(self) -> str:
        return self._NAME

    def get_population_size(self) -> int:
        pass
