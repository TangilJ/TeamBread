from ..bot_math.Vector3 import Vector3


def simple_aim(position: Vector3, target: Vector3) -> float:
    pos_to_target = target - position
    self_right = Vector3.cross_product(position, Vector3(0, 1, 0))

    if Vector3.dot_product(self_right, pos_to_target) < 0:
        return 1.0
    else:
        return -1.0
