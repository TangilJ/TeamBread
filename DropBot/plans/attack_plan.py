from rlbot.agents.base_agent import BaseAgent
from .base_plan import Plan
from DropBot.steps.base_step import BaseStep
from DropBot.steps.dribble_step import DribbleStep
from typing import List


class AttackPlan(Plan):
    def __init__(self, agent: BaseAgent):
        super().__init__(agent)
        self.steps: List[BaseStep] = [
            DribbleStep(agent)
        ]
