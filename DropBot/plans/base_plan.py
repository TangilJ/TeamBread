from rlbot.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket
from rlbot.agents.base_agent import SimpleControllerState
from ..steps.base_step import BaseStep
from typing import List, Union


class Plan:
    def __init__(self, name: str, team: int, index: int, field_info: FieldInfoPacket):
        self.name: str = name
        self.team: int = team
        self.index: int = index
        self.field_info: FieldInfoPacket = field_info

        self.cancellable: bool = True
        self.steps: List[BaseStep] = []
        self.step_index = 0

    def get_output(self, packet: GameTickPacket) -> Union[SimpleControllerState, None]:
        # Execute each step in order. If a step returns None, move on to the next step.
        output = self.steps[self.step_index].get_output(packet)
        while output is None and self.step_index < len(self.steps):
            self.step_index += 1
            output = self.steps[self.step_index].get_output(packet)

        if self.step_index > len(self.steps) - 1:
            return None

        return output
