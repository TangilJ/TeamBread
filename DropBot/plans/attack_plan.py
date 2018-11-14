from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.base_agent import BaseAgent
from .base_plan import Plan
from DropBot.steps.base_step import BaseStep
from DropBot.steps.move_step import MoveStep
from DropBot.planner.zone import Zone
from DropBot.bot_math.Vector3 import Vector3
from typing import List
from DropBot.objects.physics_object import PhysicsObject


class AttackPlan(Plan):
    def __init__(self, agent: BaseAgent, zone: Zone):
        super().__init__(agent)
        self.steps: List[BaseStep] = []
        self.sequential = False
        self.zone: Zone = zone

        self.area: Vector3 = Vector3(2500, -2250, 0)
        if zone == Zone.FOUR:
            self.area.x *= -1
        if self.agent.team == 1:  # Orange team
            self.area.y *= -1

    def decide_step(self, packet: GameTickPacket) -> BaseStep:
        ball = PhysicsObject(packet.game_ball.physics)
        ball_zone: Zone = Zone.FOUR
        ball_team: int = 0
        if ball.location.x < 0:
            ball_zone = Zone.THREE
        if ball.location.y < 0:
            ball_team = 1

        if ball_zone == self.zone and ball_team == self.agent.team:
            return MoveStep(self.agent, ball.location)
        return MoveStep(self.agent, self.area)
