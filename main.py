from src.controller import Controller
from src.model import Model

model = Model()
controller = Controller(model)

controller.game()