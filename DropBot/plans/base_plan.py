from abc import ABCMeta
from rlbot.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket
from rlbot.agents.base_agent import SimpleControllerState
from DropBot.steps.base_step import BaseStep
from typing import List, Union, Optional


class Plan(metaclass=ABCMeta):
    def __init__(self, name: str, team: int, index: int, field_info: FieldInfoPacket):
        self.name: str = name
        self.team: int = team
        self.index: int = index
        self.field_info: FieldInfoPacket = field_info

        self.cancellable: bool = True
        self.sequential: bool = True  # If True, steps are done in order. If False, steps are decided by `decide_step`.
        self.steps: List[BaseStep] = []
        self.step_index = 0
        self.current_step: Optional[BaseStep] = None

    def decide_step(self, packet: GameTickPacket) -> BaseStep:
        pass

    def get_output(self, packet: GameTickPacket) -> Union[SimpleControllerState, None]:
        if self.sequential:
            # Execute each step in order. If a step returns None, move on to the next step.
            output = self.steps[self.step_index].get_output(packet)
            while output is None and self.step_index < len(self.steps):
                output = self.steps[self.step_index].get_output(packet)
                self.step_index += 1

            if self.step_index > len(self.steps) - 1:
                return None

            return output

        else:
            if self.current_step is None:
                self.current_step = self.decide_step(packet)
            if self.current_step.cancellable:
                self.current_step = self.decide_step(packet)
                if self.current_step is None:
                    return None

            return self.current_step.get_output(packet)
