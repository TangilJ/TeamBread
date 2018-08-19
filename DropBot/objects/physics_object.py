from rlbot.utils.structures import game_data_struct
from ..bot_math.Vector3 import Vector3


class PhysicsObject:
    def __init__(self, physics: game_data_struct.Physics):
        self.location = Vector3(physics.location)
        self.velocity = Vector3(physics.velocity)
        self.rotation = Vector3(physics.rotation)
        self.angular_velocity = Vector3(physics.angular_velocity)
