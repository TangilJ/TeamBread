from .base_plan import Plan
from ..steps.base_step import BaseStep
from ..steps.dribble_step import DribbleStep
from typing import List


class ChasePlan(Plan):
    def __init__(self, name: str, team: int, index: int):
        super().__init__(name, team, index)
        self.steps: List[BaseStep] = [DribbleStep]
