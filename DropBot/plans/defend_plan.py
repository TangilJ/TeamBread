from rlbot.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket
from .base_plan import Plan
from DropBot.objects.physics_object import PhysicsObject
from DropBot.steps.base_step import BaseStep
from DropBot.steps.hover_step import HoverStep
from DropBot.steps.dribble_step import DribbleStep
from DropBot.steps.dodge_step import DodgeStep
from DropBot.utils.ball_prediction import predict_landing_pos_time
from DropBot.bot_math.Vector3 import Vector3
from typing import List


class DefendPlan(Plan):
    def __init__(self, name: str, team: int, index: int, field_info: FieldInfoPacket):
        super().__init__(name, team, index, field_info)
        self.sequential = False
        self.steps: List[BaseStep] = []

    def decide_step(self, packet: GameTickPacket) -> BaseStep:
        # If the ball is going to land on our side, go and dribble it.
        # If the is ball on their side, hover over where the most damaged areas are on our side.
        # If the bot has possession of the ball and is aiming at the other side, dodge to flick it to the other side.

        ball = PhysicsObject(packet.game_ball.physics)
        bot = PhysicsObject(packet.game_cars[self.index].physics)
        ball_landing, _ = predict_landing_pos_time(ball.location, ball.velocity)
        ball_landing_on_our_side = (self.team == 0 and ball_landing.y < 0) or (self.team == 1 and ball_landing.y > 0)

        if ball_landing_on_our_side:
            if Vector3.distance(ball.location, bot.location) < 200:
                return DodgeStep(self.name, self.team, self.index, self.field_info, ball.location)
            return DribbleStep(self.name, self.team, self.index, self.field_info)
        else:
            return HoverStep(self.name, self.team, self.index, self.field_info)
