from abc import ABC, abstractmethod

class Renderable(ABC):

    renderables = []

    def __init__(self):
        Renderable.renderables.append(self)

    @abstractmethod
    def render(self, screen, player, texture_manager):
        pass