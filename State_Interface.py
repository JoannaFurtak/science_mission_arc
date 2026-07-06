#! /usr/bin/python3
from abc import ABC, abstractmethod

class State(ABC):

    #getter
    @property
    def context(self):
        return self.contexts 

    #setter
    @context.setter
    def context(self, context):
        self.context = context

    @abstractmethod #kazdy stan ma metode step
    def step(self):
        pass

    @abstractmethod #kazdy stan ma swoja nazwe, to jest drukowanie jego nazwy
    def __repr__(self):
        pass