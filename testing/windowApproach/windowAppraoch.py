#NAME: windowApproach.py
#DATE: 12/11/2018
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python class
#COPY: Copyright 2018, All Rights Reserved, Ryan McCartney

import math
import time
import numpy as np
import numba as nb
from numba import jitclass
from numba import float64   
import matplotlib.pyplot as plt

class WindowApproach():

    show_animation = True

    def __init__(self,configuration):

         # robot parameter
        self.max_speed = 1.0  # [m/s]
        self.min_speed = -0.5  # [m/s]
        self.max_yawrate = 40.0 * math.pi / 180.0  # [rad/s]
        self.max_accel = 0.2  # [m/ss]
        self.max_dyawrate = 40.0 * math.pi / 180.0  # [rad/ss]
        self.v_reso = 0.01  # [m/s]
        self.yawrate_reso = 0.1 * math.pi / 180.0  # [rad/s]
        self.dt = 0.1  # [s]
        self.predict_time = 3.0  # [s]
        self.to_goal_cost_gain = 1.0
        self.speed_cost_gain = 1.0
        self.robot_radius = 1.0  # [m]

    @nb.jit(nopython=True)
    @staticmethod
    def motion(x, u, dt):
        
        # motion model
        x[2] += u[1] * dt
        x[0] += u[0] * math.cos(x[2]) * dt
        x[1] += u[0] * math.sin(x[2]) * dt
        x[3] = u[0]
        x[4] = u[1]

        return x

    def calc_dynamic_window(self,x):

        #Dynamic window from robot specification
        Vs = [self.min_speed, self.max_speed,
          -self.max_yawrate, self.max_yawrate]

        #Dynamic window from motion model
        Vd = [x[3] - self.max_accel * self.dt,
        x[3] + self.max_accel * self.dt,
        x[4] - self.max_dyawrate * self.dt,
        x[4] + self.max_dyawrate * self.dt]

        #[vmin,vmax, yawrate min, yawrate max]
        dw = [max(Vs[0], Vd[0]), min(Vs[1], Vd[1]),
        max(Vs[2], Vd[2]), min(Vs[3], Vd[3])]

        return dw

    @nb.jit(nopython=True)
    def calc_trajectory(self, xinit, v, y):

        x = np.array(xinit)
        traj = np.array(x)
        time = 0
    
        while time <= self.predict_time:
            x = motion(x, [v, y], self.dt)
            traj = np.vstack((traj, x))
            time += self.dt

        return traj

    def calc_final_input(self, x, u, dw, goal, ob):

        xinit = x[:]
        min_cost = 10000.0
        min_u = u
        min_u[0] = 0.0
        best_traj = np.array([x])
    
        # evalucate all trajectory with sampled input in dynamic window
        for v in np.arange(dw[0], dw[1], self.v_reso):
            for y in np.arange(dw[2], dw[3], self.yawrate_reso):
                traj = self.calc_trajectory(xinit, v, y)

                # calc cost
                to_goal_cost = calc_to_goal_cost(traj, goal)
                speed_cost = self.speed_cost_gain * \
                    (self.max_speed - traj[-1, 3])
                ob_cost = self.calc_obstacle_cost(traj, ob)
                # print(ob_cost)

                final_cost = to_goal_cost + speed_cost + ob_cost

                #print (final_cost)

                # search minimum trajectory
                if min_cost >= final_cost:
                    min_cost = final_cost
                    min_u = [v, y]
                    best_traj = traj

        return min_u, best_traj


    def calc_obstacle_cost(self, traj, ob):
        # calc obstacle cost inf: collistion, 0:free

        skip_n = 2
        minr = float("inf")

        for ii in range(0, len(traj[:, 1]), skip_n):
            for i in range(len(ob[:, 0])):
                ox = ob[i, 0]
                oy = ob[i, 1]
                dx = traj[ii, 0] - ox
                dy = traj[ii, 1] - oy

                r = math.sqrt(dx**2 + dy**2)
                if r <= self.robot_radius:
                    return float("Inf")  # collision

                if minr >= r:
                    minr = r

        return 1.0 / minr  # OK

    def calc_to_goal_cost(self, traj, goal):
        
        #Calculate to goal cost. It is 2D norm.
        goal_magnitude = math.sqrt(goal[0]**2 + goal[1]**2)
        traj_magnitude = math.sqrt(traj[-1, 0]**2 + traj[-1, 1]**2)
        dot_product = (goal[0] * traj[-1, 0]) + (goal[1] * traj[-1, 1])
        error = dot_product / (goal_magnitude * traj_magnitude)
        error_angle = math.acos(error)
        cost = self.to_goal_cost_gain * error_angle

        return cost

    def dwa_control(self, x, u, goal, ob):
        
        # Dynamic Window control
        dw = self.calc_dynamic_window(x)
        u, traj = self.calc_final_input(x, u, dw, goal, ob)
    
        return u, traj

    @staticmethod
    def plot_arrow(x, y, yaw, length=0.5, width=0.1):
        plt.arrow(x, y, length * math.cos(yaw), length * math.sin(yaw), head_length=width, head_width=width)
        plt.plot(x, y)