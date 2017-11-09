from abc import ABC, abstractmethod

from typing import Tuple, List


class Model(ABC):

    @abstractmethod
    def run(self) -> Tuple[List[float], List[float], List[float]]:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_population_size(self) -> int:
        pass
