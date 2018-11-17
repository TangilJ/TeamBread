from Bread.bot_math.Vector3 import Vector3
from rlbot.agents.base_agent import SimpleControllerState
import math

SPEED_MATCH = 1.3  # How quickly the speed should match the target speed in `arrive_on_time`


def simple_aim(position: Vector3, yaw: float, target: Vector3) -> float:
    pos_to_target = target - position
    facing = Vector3(math.cos(yaw), math.sin(yaw), 0)
    self_right = Vector3.cross_product(facing, Vector3(0, 0, 1))

    if Vector3.dot_product(self_right, pos_to_target) < 0:
        return 1.0
    else:
        return -1.0


# Used to arrive at the `target` in `time_taken` seconds, starting from `position` with `velocity`.
def arrive_on_time(position: Vector3, velocity: Vector3, target: Vector3, time_taken: float) -> SimpleControllerState:
    to_target = target - position
    distance = to_target.magnitude()
    average_speed = distance / (time_taken + 0.0000001)
    current_speed = velocity.magnitude()
    target_speed = (1 - SPEED_MATCH) * current_speed + SPEED_MATCH * average_speed

    controller = SimpleControllerState()

    if current_speed < target_speed:
        controller.throttle = 1
        controller.boost = target_speed > 1410
    else:
        controller.boost = False
        if current_speed - target_speed > 75:
            controller.throttle = -1
        else:
            controller.throttle = 0

    if current_speed < 100:
        controller.throttle = 0.2

    return controller
