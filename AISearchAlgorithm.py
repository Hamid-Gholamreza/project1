from abc import ABC , abstractclassmethod

class AISearchAlgorithm(ABC):
    @abstractclassmethod
    def _making_node():
        pass
    @abstractclassmethod

    def _expand():
        pass
    @abstractclassmethod

    def _goal_test():
        pass

    @abstractclassmethod
    def _adjacent_generator_for_BF1():
        pass

    @abstractclassmethod
    def _barricade_checking():
        pass