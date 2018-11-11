from rlbot.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket
from DropBot.plans.move_plan import MovePlan
from DropBot.plans.defend_plan import DefendPlan
from DropBot.plans.dribble_plan import DribblePlan
from DropBot.plans.base_plan import Plan
from DropBot.bot_math.Vector3 import Vector3
from .zone import Zone


class PlanChooser:
    def __init__(self, name: str, team: int, index: int, field_info: FieldInfoPacket):
        self.name: str = name
        self.team: int = team
        self.index: int = index
        self.field_info: FieldInfoPacket = field_info
        self.plan_args = (name, team, index, field_info)
        self.current_plan: Plan = DefendPlan(*self.plan_args)
        self.on_kickoff: bool = False
        self.zone: Zone = Zone.ONE_AND_TWO

    def choose_plan(self, packet: GameTickPacket) -> Plan:
        ball = packet.game_ball.physics.location

        if -10 < ball.x < 10 and -1 < ball.y < 1:
            if not self.on_kickoff:
                self.on_kickoff = True
                self.current_plan = self.__choose_kickoff_plan(packet)
        else:
            if self.on_kickoff:
                self.on_kickoff = False
                self.current_plan = self.__choose_new_plan(packet)

        return self.current_plan

    def __choose_new_plan(self, packet: GameTickPacket) -> Plan:
        # TODO: Finish this method. Zone.ONE_AND_TWO sticks to DefendPlan.
        # TODO: Zone.THREE and Zone.FOUR stick to a new AttackPlan.
        return DribblePlan(*self.plan_args)

    def __choose_kickoff_plan(self, packet: GameTickPacket) -> Plan:
        is_on_diagonal = False
        teammate_on_diagonal = False
        bot_loc = Vector3(packet.game_cars[self.index].physics.location)

        # For every bot in our team
        for i in range(3 * self.team, 3 * (self.team + 1)):
            location = packet.game_cars[i].physics.location
            # We are using ranges instead of exact values because the game engine will not always have the exact value.
            if 1860 < abs(location.x) < 1870 and 2375 < abs(location.y) < 2385:
                if i == self.index:
                    is_on_diagonal = True
                else:
                    teammate_on_diagonal = True

        # On a kickoff, the bot goes to the ball if:
        # - It's the only one on a diagonal kickoff
        # - Or if the bot is on the left for blue, or the right for orange
        # (The second point is arbitrary but it's a good way to not double commit on the ball on kickoff)
        #
        # If it's not going for kickoff and it's the closest to the other side compared to the other non-kickoff bot,
        # it will go to the opponent's side and chill there waiting for the ball to be passed to it.
        #
        # The remaining bot will stay on its side.
        team_side_y = 1200 * (1 if self.team else -1)
        if is_on_diagonal:
            if not teammate_on_diagonal:
                self.zone = Zone.THREE
                return DribblePlan(*self.plan_args)
            else:
                if bot_loc.x > 0:
                    self.zone = Zone.THREE
                    return DribblePlan(*self.plan_args)
                else:
                    self.zone = Zone.FOUR
                    opponent_side = Vector3(bot_loc.x, -team_side_y, bot_loc.z)
                    return MovePlan(*self.plan_args, opponent_side)
        else:
            self.zone = Zone.ONE_AND_TWO
            team_side = Vector3(bot_loc.x, team_side_y, bot_loc.z)
            return MovePlan(*self.plan_args, team_side)
