from rlbot.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from .base_step import BaseStep
from DropBot.objects.physics_object import PhysicsObject
from DropBot.utils import steering
from DropBot.bot_math.Vector3 import Vector3


class MoveStep(BaseStep):
    def __init__(self, agent: BaseAgent, target: Vector3):
        super().__init__(agent)
        self.target: Vector3 = target

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        bot = PhysicsObject(packet.game_cars[self.agent.index].physics)
        steer = steering.simple_aim(bot.location, bot.rotation.z, self.target)

        controller = SimpleControllerState()
        controller.steer = steer
        controller.throttle = 1

        return controller
