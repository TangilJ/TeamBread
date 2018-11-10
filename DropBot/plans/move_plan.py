from rlbot.utils.structures.game_data_struct import FieldInfoPacket
from .base_plan import Plan
from DropBot.steps.base_step import BaseStep
from DropBot.steps.move_step import MoveStep
from DropBot.bot_math.Vector3 import Vector3
from typing import List


class MovePlan(Plan):
    def __init__(self, name: str, team: int, index: int, field_info: FieldInfoPacket, target: Vector3):
        super().__init__(name, team, index, field_info)
        self.steps: List[BaseStep] = [
            MoveStep(name, team, index, field_info, target)
        ]
