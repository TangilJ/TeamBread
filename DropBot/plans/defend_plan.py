from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.base_agent import BaseAgent
from .base_plan import Plan
from DropBot.objects.physics_object import PhysicsObject
from DropBot.steps.base_step import BaseStep
from DropBot.steps.hover_step import HoverStep
from DropBot.steps.dribble_step import DribbleStep
from DropBot.steps.simple_dribble_step import SimpleDribbleStep
from DropBot.steps.dodge_step import DodgeStep
from DropBot.utils.ball_prediction import predict_landing_pos_time
from DropBot.bot_math.Vector3 import Vector3
from typing import List, Optional
import math


class DefendPlan(Plan):
    def __init__(self, agent: BaseAgent):
        super().__init__(agent)
        self.sequential = False
        self.steps: List[BaseStep] = []
        self.dodge_step: Optional[DodgeStep] = None

    def decide_step(self, packet: GameTickPacket) -> BaseStep:
        # If the ball is going to land on our side, go and dribble it.
        # If the is ball on their side, hover over where the most damaged areas are on our side.
        # If the bot has possession of the ball and is aiming at the other side, dodge to flick it to the other side.

        ball = PhysicsObject(packet.game_ball.physics)
        bot = PhysicsObject(packet.game_cars[self.agent.index].physics)
        ball_landing, _ = predict_landing_pos_time(ball.location, ball.velocity)
        ball_landing_on_our_side = (self.agent.team == 0 and ball_landing.y < 0) or (self.agent.team == 1 and ball_landing.y > 0)

        # Dodge if dodging is in progress and it is not going to expire. Else, expire dodge_step if it isn't already.
        if self.dodge_step is not None:  # Is dodging in progress?
            if self.dodge_step.get_output(packet) is not None:  # Is it going to expire this frame?
                return self.dodge_step
            else:
                self.dodge_step = None  # Expire dodge_step

        if ball_landing_on_our_side:
            # If carrying the ball
            if Vector3.distance(ball.location, bot.location) < 300:
                # If the bot is facing the opponents' side, dodge into the ball. Else, dribble it.
                if (1/4*math.pi < bot.rotation.z < 3/4*math.pi) if self.agent.team == 0 else (-3/4*math.pi < bot.rotation.z < -1/4*math.pi):
                    # Instantiate a new DodgeStep if the previous one expired
                    if self.dodge_step is None:
                        self.dodge_step = DodgeStep(self.agent, ball.location)
                    return self.dodge_step
                return DribbleStep(self.agent, ball.location)
            return SimpleDribbleStep(self.agent)
        else:
            # Stay on our side if the ball is on the opponents' side
            return HoverStep(self.agent)
