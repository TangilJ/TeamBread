from rlbot.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from .base_step import BaseStep
from DropBot.bot_math.Vector3 import Vector3
from DropBot.objects.physics_object import PhysicsObject
from typing import Optional
import math


class DodgeStep(BaseStep):
    def __init__(self, agent: BaseAgent, target: Vector3, dodge_time: float = 0.2):
        super().__init__(agent)
        self.target: Vector3 = target
        self.cancellable: bool = False

        self.on_second_jump = False
        self.next_dodge_time = 0
        self.dodge_time = dodge_time

    def get_output(self, packet: GameTickPacket) -> Optional[SimpleControllerState]:
        controller = SimpleControllerState()
        bot = PhysicsObject(packet.game_cars[self.agent.index].physics)

        if packet.game_info.seconds_elapsed > self.next_dodge_time:
            controller.jump = True

            # Calculate pitch and roll based on target and bot position

            # Correct yaw from (0 to pi to -pi to 0), to (0 to 2pi).
            # Then rotate circle by pi/2 degrees. Then flip circle vertically.
            yaw = bot.rotation.z
            if yaw < 0:
                yaw += 2 * math.pi
            yaw -= math.pi / 2
            if yaw < 0:
                yaw += 2 * math.pi
            yaw = 2 * math.pi - yaw

            direction_to_target = (self.target - bot.location).normalised()
            angle_to_target = math.atan2(direction_to_target.y, direction_to_target.x)
            angle = angle_to_target - yaw

            controller.pitch = -math.cos(angle)
            controller.roll = math.sin(angle)

            if self.on_second_jump:
                return None
            else:
                self.on_second_jump = True
                self.next_dodge_time = packet.game_info.seconds_elapsed + self.dodge_time
        else:
            controller.jump = False

        return controller
