from rlbot.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket
from .base_plan import Plan
from DropBot.objects.physics_object import PhysicsObject
from DropBot.steps.base_step import BaseStep
from DropBot.steps.hover_step import HoverStep
from DropBot.steps.dribble_step import DribbleStep
from typing import List


class DefendPlan(Plan):
    def __init__(self, name: str, team: int, index: int, field_info: FieldInfoPacket):
        super().__init__(name, team, index, field_info)
        self.sequential = False
        self.steps: List[BaseStep] = [
            HoverStep(name, team, index, field_info),
            DribbleStep(name, team, index, field_info)
        ]

    def decide_step(self, packet: GameTickPacket) -> int:
        # If the ball is on our side, dribble it. Else if the is ball on their side, hover.
        ball = PhysicsObject(packet.ball.physics)
        ball_on_our_side = (self.team == 0 and ball.location.y < 0) or (self.team == 1 and ball.location.y > 0)

        if ball_on_our_side:
            return 1  # Index of the DribbleStep
        else:
            return 0  # Index of the HoverStep
