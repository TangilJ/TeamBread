from rlbot.agents.base_agent import BaseAgent
from .base_plan import Plan
from Bread.steps.base_step import BaseStep
from Bread.steps.dribble_step import DribbleStep
from typing import List
from Bread.bot_math.Vector3 import Vector3


class DribblePlan(Plan):
    def __init__(self, agent: BaseAgent, target: Vector3):
        super().__init__(agent)
        self.steps: List[BaseStep] = [
            DribbleStep(agent, target)
        ]
