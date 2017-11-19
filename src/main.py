from src import exporting
from src.model.continuous_time_model import ContinuousTimeModel
from src.model.discrete_time_model import DiscreteTimeModel

NUMBER_OF_DAYS = 10000
POPULATION_SIZE = 300
NUMBER_OF_SYRINGES = 10


def main():
    model1 = DiscreteTimeModel(NUMBER_OF_DAYS, POPULATION_SIZE, NUMBER_OF_SYRINGES)
    model2 = ContinuousTimeModel(NUMBER_OF_DAYS, POPULATION_SIZE, NUMBER_OF_SYRINGES)
    exporting.save_comparison(model1, model2, "HIV spread")


if __name__ == "__main__":
    main()
