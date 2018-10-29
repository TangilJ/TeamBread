from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.base_agent import SimpleControllerState
from .base_step import BaseStep
from DropBot.objects.physics_object import PhysicsObject
from DropBot.utils import steering


class ChaseStep(BaseStep):
    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        ball = PhysicsObject(packet.ball.physics)
        bot = PhysicsObject(packet.players[self.index].physics)
        steer = steering.simple_aim(bot.location, ball.location)

        controller = SimpleControllerState()
        controller.steer = steer

        return controller
