from abc import ABC, abstractmethod
from typing import Union


class Vehicle(ABC):
    def __init__(self, model='unknown'):
        self.model = model

    @abstractmethod
    def move(self, distance: Union[int, float]):
        pass


class Car(Vehicle):
    def move(self, distance: Union[int, float]):
        if isinstance(distance, int or float) is False:
            pass
        elif distance < 0:
            pass
        else:
            print('Автомобиль проехал %s километров' % distance)


class Boat(Vehicle):
    def move(self, distance: Union[int, float]):
        if isinstance(distance, int or float) is False:
            pass
        elif distance < 0:
            pass
        else:
            print('Лодка проплыла %s километров' % distance)
