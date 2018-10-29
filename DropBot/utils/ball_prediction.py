import math
from DropBot.bot_math.Vector3 import Vector3
from typing import Tuple

GROUND_Z_AXIS = 92
GRAVITY = 650


def predict_landing_pos_time(position: Vector3, velocity: Vector3) -> Tuple[Vector3, float]:
    distance_ball_to_ground = GROUND_Z_AXIS - position.z
    a = velocity.z ** 2 / GRAVITY ** 2
    b = 2 * distance_ball_to_ground / GRAVITY
    quadratic = math.sqrt(a - b)
    flight_time = velocity.z / GRAVITY + quadratic
    distance_covered_x = velocity.x * flight_time
    distance_covered_y = velocity.y * flight_time

    landing_pos = position + Vector3(distance_covered_x, distance_covered_y, distance_ball_to_ground)

    return landing_pos, flight_time
