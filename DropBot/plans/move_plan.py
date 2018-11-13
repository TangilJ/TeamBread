from rlbot.agents.base_agent import BaseAgent
from .base_plan import Plan
from DropBot.steps.base_step import BaseStep
from DropBot.steps.move_step import MoveStep
from DropBot.bot_math.Vector3 import Vector3
from typing import List


class MovePlan(Plan):
    def __init__(self, agent: BaseAgent, target: Vector3):
        super().__init__(agent)
        self.steps: List[BaseStep] = [
            MoveStep(agent, target)
        ]
