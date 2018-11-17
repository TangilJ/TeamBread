import math
from rlbot.utils.structures.ball_prediction_struct import BallPrediction
from Bread.bot_math.Vector3 import Vector3
from typing import Tuple, List

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


def get_ground_bounces(path: BallPrediction) -> List[Tuple[Vector3, float]]:
    ground_bounces: List[Tuple[Vector3, float]] = []
    for i in range(1, path.num_slices):
        prev_ang_v = path.slices[i - 1].physics.angular_velocity
        prev_norm_ang_vel = (math.sqrt(prev_ang_v.x ** 2 + prev_ang_v.y ** 2 + prev_ang_v.z ** 2))
        current_slice = path.slices[i]
        current_ang_v = current_slice.physics.angular_velocity
        current_norm_ang_vel = (math.sqrt(current_ang_v.x ** 2 + current_ang_v.y ** 2 + current_ang_v.z ** 2))
        if prev_norm_ang_vel != current_norm_ang_vel and current_slice.physics.location.z < 125:
            ground_bounces.append((Vector3(current_slice.physics.location), current_slice.game_seconds))

    return ground_bounces
