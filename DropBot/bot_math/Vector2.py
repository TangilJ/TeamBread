import rlbot.utils.structures.game_data_struct as game_data_struct
import math
from typing import Tuple, Optional
from . import Number, VectorArgument


class Vector2:
    def __init__(self, x: VectorArgument, y: Optional[Number] = None):
        self.x: Number = 0
        self.y: Number = 0

        from .Vector3 import Vector3
        if isinstance(x, game_data_struct.Vector3):
            self.x = x.x
            self.y = x.y
        elif isinstance(x, Vector2):
            self.x = x.x
            self.y = x.y
        elif isinstance(x, Vector3):
            self.x = x.x
            self.y = x.y
        elif isinstance(x, game_data_struct.Rotator):
            self.x = x.roll
            self.y = x.pitch
        elif y is not None:
            self.x = x
            self.y = y
        else:
            raise TypeError("Wrong type given for Vector2.y")

    def __add__(self, v: "Vector2") -> "Vector2":
        return Vector2(self.x + v.x, self.y + v.y)
    
    def __sub__(self, v: "Vector2") -> "Vector2":
        return Vector2(self.x - v.x, self.y - v.y)
    
    def __mul__(self, v: Number) -> "Vector2":
        return Vector2(self.x * v, self.y * v)
    
    def __truediv__(self, v: Number) -> "Vector2":
        return Vector2(self.x / v, self.y / v)
    
    def __rmul__(self, v: Number) -> "Vector2":
        return Vector2(self.x * v, self.y * v)
    
    def __rtruediv__(self, v: Number) -> "Vector2":
        return Vector2(self.x / v, self.y / v)
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return self.__str__()
    
    def magnitude(self) -> Number:
        return abs(math.sqrt(self.x**2 + self.y**2))
    
    def normalised(self) -> "Vector2":
        mag = self.magnitude()
        return Vector2(self.x / mag, self.y / mag)

    def to_tuple(self) -> Tuple[Number, Number]:
        return self.x, self.y
    
    @staticmethod
    def dot_product(v1: "Vector2", v2: "Vector2") -> Number:
        return v1.x * v2.x + v1.y * v2.y
    
    @staticmethod
    def reflect(vector: "Vector2", normal: "Vector2") -> "Vector2":
        dot = Vector2.dot_product(vector, normal)
        return Vector2(vector.x - 2 * dot * normal.x,
                       vector.y - 2 * dot * normal.y)

    @staticmethod
    def distance(p1: "Vector2", p2: "Vector2") -> Number:
        return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

    @staticmethod
    def angle(v1: "Vector2", v2: "Vector2") -> Number:
        raise NotImplementedError("angle method not yet implemented")
