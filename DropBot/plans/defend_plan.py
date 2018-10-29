from rlbot.utils.structures.game_data_struct import FieldInfoPacket
from .base_plan import Plan
from ..steps.base_step import BaseStep
from ..steps.hover_step import HoverStep
from typing import List


class DefendPlan(Plan):
    def __init__(self, name: str, team: int, index: int, field_info: FieldInfoPacket):
        super().__init__(name, team, index, field_info)
        self.steps: List[BaseStep] = [HoverStep]
