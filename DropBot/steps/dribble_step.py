from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.base_agent import SimpleControllerState
from .base_step import BaseStep
from DropBot.objects.physics_object import PhysicsObject
from DropBot.utils import steering, ball_prediction


class DribbleStep(BaseStep):
    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        controller = SimpleControllerState()

        ball = PhysicsObject(packet.game_ball.physics)
        bot = PhysicsObject(packet.game_cars[self.index].physics)

        landing, flight_time = ball_prediction.predict_landing_pos_time(ball.location, ball.velocity)
        out = steering.arrive_on_time(bot.location, bot.velocity, landing, flight_time)
        controller.throttle = out.throttle
        controller.boost = out.boost
        controller.steer = steering.simple_aim(bot.location, bot.rotation.z, landing)

        return controller
