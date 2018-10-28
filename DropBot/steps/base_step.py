from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.base_agent import SimpleControllerState
from typing import Union


class BaseStep:
    def __init__(self, name: str, team: int, index: int):
        self.name: str = name
        self.team: int = team
        self.index: int = index

        self.cancellable: bool = True

    def get_output(self, packet: GameTickPacket) -> Union[SimpleControllerState, None]:
        pass
