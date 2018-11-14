from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from .base_step import BaseStep
from DropBot.bot_math import Vector3
from DropBot.bot_math.Vector2 import Vector2
from DropBot.objects.physics_object import PhysicsObject
from DropBot.utils import steering, ball_prediction
# dribble imports
import math
import numpy as np

p_s = 0.


class DribbleStep(BaseStep):
    def __init__(self, agent: BaseAgent, target: Vector3):
        super().__init__(agent)
        self.target: Vector3 = target

    def aim(self, ball_x, ball_y, ball_z, ball_vel_x, ball_vel_y, target_x, target_y):

        # functions for finding angle between two vectors
        def unit_vector(vector):
            return vector / np.linalg.norm(vector)

        def angle_between(v1, v2):
            v1_u = unit_vector(v1)
            v2_u = unit_vector(v2)
            return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

        # direction of target relative to center of car (where should we aim)
        target = Vector2(target_x, target_y)
        angle_between_bot_and_target = math.atan2(target.y - self.bot_pos.y,
                                                  target.x - self.bot_pos.x)
        distance_to_target = math.sqrt(
            ((math.fabs(target.y - self.bot_pos.y)) ** 2 + (math.fabs(target.x - self.bot_pos.x)) ** 2))

        # direction of target relative to yaw of car (where should we aim verse where we are aiming)
        angle_front_to_target = angle_between_bot_and_target - self.bot_yaw

        # Remap angles between +/- pi
        if angle_front_to_target < -math.pi:
            angle_front_to_target += 2 * math.pi
        if angle_front_to_target > math.pi:
            angle_front_to_target -= 2 * math.pi

        # direction of ball relative to center of car (where should we aim)
        angle_between_bot_and_ball = math.atan2(ball_y - self.bot_pos.y, ball_x - self.bot_pos.x)
        # direction of ball relative to yaw of car (where should we aim verse where we are aiming)
        angle_front_to_ball = angle_between_bot_and_ball - self.bot_yaw

        # distance between bot and ball
        distance = math.sqrt(
            ((math.fabs(ball_y - self.bot_pos.y)) ** 2 + (math.fabs(ball_x - self.bot_pos.x)) ** 2))

        # direction of ball velocity relative to yaw of car (which way the ball is moving verse which way we are moving)
        ball_angle_to_car = math.atan2(ball_vel_y, ball_vel_x) - self.bot_yaw

        # similar to ball_angle_to_car but uses bot velocity vector instead
        ball_bot_angle = angle_between((ball_vel_x, ball_vel_y), (self.bot_vel.x, self.bot_vel.y))

        # magnitude of ball_bot_angle (squared)
        ball_bot_diff = (ball_vel_x ** 2 + ball_vel_y ** 2) - (self.bot_vel.x ** 2 + self.bot_vel.y ** 2)

        # p is the distance between ball and car
        # i is the magnitude of the ball's velocity (squared) the i term would normally
        # be the integral of p over time, but the ball's velocity is essentially that number
        # d is the relative speed between ball and car
        # note that bouncing a ball is distinctly different than balancing something that doesnt bounce

        p = 0.
        i = 0.
        d = 0.

        # p_s is the x component of the distance to the ball
        # d_s is the one frame change of p_s, that's why p_s has to be global
        global p_s
        d_s = 0.

        # speed of car to be used when deciding how much to accelerate when approaching the ball
        car_speed = math.sqrt(self.bot_vel.x ** 2 + self.bot_vel.y ** 2)

        # Remap angles between +/- pi
        if angle_front_to_ball < -math.pi:
            angle_front_to_ball += 2 * math.pi
        if angle_front_to_ball > math.pi:
            angle_front_to_ball -= 2 * math.pi

        if ball_angle_to_car < -math.pi:
            ball_angle_to_car += 2 * math.pi
        if ball_angle_to_car > math.pi:
            ball_angle_to_car -= 2 * math.pi

        # we modify distance and ball_bot_diff so that only the component along the car's path is counted
        # if the ball is too far to the left, we don't want the bot to think it has to drive forward
        # to catch it
        distance_y = math.fabs(distance * math.cos(angle_front_to_ball))
        distance_x = math.fabs(distance * math.sin(angle_front_to_ball))
        ball_bot_diff_y = ball_bot_diff * math.cos(angle_front_to_ball)
        ball_bot_diff_x = ball_bot_diff * math.sin(angle_front_to_ball)

        # ball moving forward WRT car yaw?
        forward = False
        if math.fabs(ball_angle_to_car) < math.radians(90):
            forward = True

        # this section is the standard approach to a dribble
        # the car quickly gets to the general area of the ball, then drives slow until it is very close
        # then begins balancing
        if (distance > 90000):  # 900
            self.controller.throttle = 1.
            self.controller.boost = False
        # we limit the speed to 300 to ensure a slow approach
        elif distance > 40000 and car_speed > 300:
            self.controller.throttle = 0
        elif (distance > 40000): # 400
            self.controller.throttle = .1
            self.controller.boost = False

        # this is the balancing PID section
        # it always starts with full boost/throttle because the bot thinks the ball is too far in front
        # opposite is true for behind
        else:
            # first we give the distance values signs
            if forward == True:
                d = ball_bot_diff
                i = (ball_vel_x ** 2 + ball_vel_y ** 2)
            else:
                d = -ball_bot_diff
                i = -(ball_vel_x ** 2 + ball_vel_y ** 2)

            if math.fabs(math.degrees(angle_front_to_ball)) < 90:
                p = distance_y

            else:
                p = -1 * distance_y

            # this is the PID correction.  all of the callibration goes on right here
            # there is literature about how to set the variables but it doesn't work quite the same
            # because the car is only touching the ball (and interacting with the system) on bounces
            # we run the PID formula through tanh to give a value between -1 and 1 for steering input

            # if the ball is lower we have no velocity bias
            bias_v = 600000 #600000

            # just the basic PID if the ball is too low
            if ball_z < 120:
                correction = np.tanh((20 * p + .0015 * (i) + .006 * d) / 500) #np.tanh((20 * p + .0015 * (i) + .006 * d) / 500)
            # if the ball is on top of the car we use our bias (the bias is in velocity units squared)
            else:
                correction = np.tanh((20 * p + .0015 * (i - bias_v) + .006 * d) / 500)

            # makes sure we don't get value over .99 so we dont exceed maximum thrust
            self.controller.throttle = correction * .99

            # anything over .9 is boost
            if correction > .99:
                self.controller.boost = True
            else:
                self.controller.boost = False

        # this is the PID steering section
        # p_s is the x component of the distance to the ball (relative to the cars direction)
        # d_s is the on frame change in p_s

        # we use absolute value and then set the sign later
        d_s = math.fabs(p_s) - math.fabs(distance_x)
        p_s = math.fabs(distance_x)

        # give the values the correct sign
        if angle_front_to_ball < 0:
            p_s = -p_s
            d_s = -d_s
        # d_s is actually -d_s ...whoops
        d_s = -d_s

        # set the bias depending on keypress
        # 'a' makes the car dribble counterclockwise, 'd' for clockwise
        bias = 0.
        # if keyboard.is_pressed('a'):
        #     bias = 45
        # elif keyboard.is_pressed('d'):
        #     bias = -45

        #print(angle_front_to_target)
        min_angle = 10
        max_bias = 45
        if angle_front_to_target < math.radians(-min_angle):
            # If the target is more than 10 degrees right from the centre, steer left
            bias = max_bias
        elif angle_front_to_target > math.radians(min_angle):
            # If the target is more than 10 degrees left from the centre, steer right
            bias = -max_bias
        else:
            # If the target is less than 10 degrees from the centre, steer straight
            bias = max_bias * (math.degrees(angle_front_to_target)/min_angle)

        # the correction settings can be altered to change performance
        correction = np.tanh((100 * (p_s + bias) + 1500 * d_s) / 8000)

        # apply the correction
        self.controller.steer = correction
        # ToDo: use ball velocity to get the anlge
        # print(distance_to_target)
        # print(angle_front_to_target)
        if distance_to_target < 1000 and -math.pi/3 < angle_front_to_target < math.pi/3 and distance < 500:
            self.controller.throttle = -1
            self.controller.boost = 0

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        self.controller: SimpleControllerState = SimpleControllerState()

        # Update game data variables
        self.bot_yaw = packet.game_cars[self.agent.team].physics.rotation.yaw
        self.bot_pos = packet.game_cars[self.agent.index].physics.location
        self.bot_vel = packet.game_cars[self.agent.index].physics.velocity

        ball_pos = packet.game_ball.physics.location
        ball_vel = packet.game_ball.physics.velocity
        # print(dir(packet.game_cars[1]))
        # events = npt.get_gamepad()
        # Todo: add a way to change target
        target_x = 0
        target_y = 0
        self.aim(ball_pos.x, ball_pos.y, ball_pos.z, ball_vel.x, ball_vel.y, target_x, target_y)

        return self.controller
