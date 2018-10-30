import rlbot.utils.structures.game_data_struct as game_data_struct
from typing import Union
from .Vector3 import Vector3
from .Vector2 import Vector2

Number = Union[int, float]
VectorArgument = Union[Number, game_data_struct.Vector3, game_data_struct.Rotator, Vector2, Vector3]
