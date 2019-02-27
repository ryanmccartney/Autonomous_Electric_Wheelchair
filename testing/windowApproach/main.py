#NAME: main.py
#DATE: 12/11/2018
#AUTH: Ryan McCartney, EEE Undergraduate, Queen's University Belfast
#DESC: A python class for moving the wheelchair in a circle whilst avoiding collisoins
#COPY: Copyright 2018, All Rights Reserved, Ryan McCartney

from windowApproach import windowAppraoch
import json
import time

    print(__file__ + " start!!")
    # initial state [x(m), y(m), yaw(rad), v(m/s), omega(rad/s)]
    x = np.array([0.0, 0.0, math.pi / 8.0, 0.0, 0.0])
    # goal position [x(m), y(m)]
    goal = np.array([10, 10])
    # obstacles [x(m) y(m), ....]
    ob = np.array([[-1, -1],
                   [0, 2],
                   [4.0, 2.0],
                   [5.0, 4.0],
                   [5.0, 5.0],
                   [5.0, 6.0],
                   [5.0, 9.0],
                   [8.0, 9.0],
                   [7.0, 9.0],
                   [12.0, 12.0]
                   ])

    u = np.array([0.0, 0.0])
    config = Config()
    traj = np.array(x)

    for i in range(1000):

        start = time.time()
        u, ltraj = dwa_control(x, u, config, goal, ob)
        x = motion(x, u, config.dt)
        traj = np.vstack((traj, x))  # store state history
        end = time.time()

        print("STATUS: The current trajectory is set as '",x,"'. Processing  took %.2f seconds." % round((end-start),2))
 
        if show_animation:
            start = time.time()
            plt.cla()
            plt.plot(ltraj[:, 0], ltraj[:, 1], "-g")
            plt.plot(x[0], x[1], "xr")
            plt.plot(goal[0], goal[1], "xb")
            plt.plot(ob[:, 0], ob[:, 1], "ok")
            plot_arrow(x[0], x[1], x[2])
            plt.axis("equal")
            plt.grid(True)
            plt.pause(0.0001)
            end = time.time()
            print("STATUS: Plotting the animation took %.2f seconds." % round((end-start),2))

        # check goal
        if math.sqrt((x[0] - goal[0])**2 + (x[1] - goal[1])**2) <= config.robot_radius:
            print("Goal!!")
            break

    print("Done")
    if show_animation:
        plt.plot(traj[:, 0], traj[:, 1], "-r")
        plt.pause(0.0001)

    plt.show()

