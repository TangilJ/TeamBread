from abc import ABCMeta, abstractmethod
from rlbot.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket
from rlbot.agents.base_agent import SimpleControllerState
from typing import Union


class BaseStep(metaclass=ABCMeta):
    def __init__(self, name: str, team: int, index: int, field_info: FieldInfoPacket):
        self.name: str = name
        self.team: int = team
        self.index: int = index
        self.field_info: FieldInfoPacket = field_info

        self.cancellable: bool = True

    @abstractmethod
    def get_output(self, packet: GameTickPacket) -> Union[SimpleControllerState, None]:
        pass
