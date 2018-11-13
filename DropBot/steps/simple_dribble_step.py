from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.base_agent import SimpleControllerState
from .base_step import BaseStep
from DropBot.objects.physics_object import PhysicsObject
from DropBot.utils import steering, ball_prediction


class SimpleDribbleStep(BaseStep):
    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        controller = SimpleControllerState()

        bot = PhysicsObject(packet.game_cars[self.agent.index].physics)

        landing, flight_time = ball_prediction.get_ground_bounces(self.agent.get_ball_prediction_struct())[0]
        out = steering.arrive_on_time(bot.location, bot.velocity, landing,
                                      flight_time - packet.game_info.seconds_elapsed)
        controller.throttle = out.throttle
        controller.boost = out.boost
        controller.steer = steering.simple_aim(bot.location, bot.rotation.z, landing)

        return controller