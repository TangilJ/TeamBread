from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.base_agent import BaseAgent
from .base_plan import Plan
from Bread.steps.base_step import BaseStep
from Bread.steps.simple_dribble_step import SimpleDribbleStep
from Bread.steps.move_step import MoveStep
from Bread.planner.zone import Zone
from Bread.bot_math.Vector3 import Vector3
from typing import List
from Bread.objects.physics_object import PhysicsObject


class AttackPlan(Plan):
    def __init__(self, agent: BaseAgent, zone: Zone):
        super().__init__(agent)
        self.steps: List[BaseStep] = []
        self.sequential = False
        self.zone: Zone = zone

        self.area: Vector3 = Vector3(2500, 2250, 0)
        if zone == Zone.FOUR:
            self.area.x *= -1
        if self.agent.team == 1:  # Orange team
            self.area.y *= -1

    def decide_step(self, packet: GameTickPacket) -> BaseStep:
        ball = PhysicsObject(packet.game_ball.physics)
        ball_zone: Zone = Zone.THREE
        ball_team: int = 0
        if ball.location.x < 0:
            ball_zone = Zone.FOUR
        if ball.location.y < 0:
            ball_team = 1

        if ball_zone == self.zone and ball_team == self.agent.team:
            return SimpleDribbleStep(self.agent, 0.2)
        return MoveStep(self.agent, self.area)
