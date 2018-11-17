from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from Bread.planner.plan_chooser import PlanChooser


class Bread(BaseAgent):
    def initialize_agent(self) -> None:
        self.plan_chooser: PlanChooser = PlanChooser(self)

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        plan = self.plan_chooser.choose_plan(packet)
        out = plan.get_output(packet)

        return out
