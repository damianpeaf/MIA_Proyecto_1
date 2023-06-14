from abc import ABC, abstractmethod


class Observable:

    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, data):
        for observer in self.observers:
            observer.update(data)


class Observer(ABC):

    @abstractmethod
    def update(self, data):
        pass
