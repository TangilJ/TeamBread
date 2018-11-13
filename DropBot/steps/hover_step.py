from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.base_agent import SimpleControllerState
from .base_step import BaseStep
from DropBot.objects.physics_object import PhysicsObject
from DropBot.utils import steering, tile_average
from DropBot.bot_math.Vector3 import Vector3


class HoverStep(BaseStep):
    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        controller = SimpleControllerState()

        bot = PhysicsObject(packet.game_cars[self.agent.index].physics)
        average: Vector3 = tile_average.get_tile_average(packet, self.agent.get_field_info())

        controller.throttle = 1
        controller.boost = False
        controller.steer = steering.simple_aim(bot.location, bot.rotation.z, average)

        return controller
