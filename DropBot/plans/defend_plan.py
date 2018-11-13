from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.base_agent import BaseAgent
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
    def __init__(self, agent: BaseAgent):
        super().__init__(agent)
        self.sequential = False
        self.steps: List[BaseStep] = []

    def decide_step(self, packet: GameTickPacket) -> BaseStep:
        # If the ball is going to land on our side, go and dribble it.
        # If the is ball on their side, hover over where the most damaged areas are on our side.
        # If the bot has possession of the ball and is aiming at the other side, dodge to flick it to the other side.

        ball = PhysicsObject(packet.game_ball.physics)
        bot = PhysicsObject(packet.game_cars[self.agent.index].physics)
        ball_landing, _ = predict_landing_pos_time(ball.location, ball.velocity)
        ball_landing_on_our_side = (self.agent.team == 0 and ball_landing.y < 0) or (self.agent.team == 1 and ball_landing.y > 0)

        if ball_landing_on_our_side:
            if Vector3.distance(ball.location, bot.location) < 200:
                return DodgeStep(self.agent, ball.location)
            return DribbleStep(self.agent)
        else:
            return HoverStep(self.agent.name)
