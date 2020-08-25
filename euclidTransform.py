import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math


def euclidTrans(xyzs: list, space: list):
    fig = plt.figure()
    ax = mplot3d.Axes3D(fig)

    xyzs = np.array(xyzs)
    # xyzs[:50, 2:] = xyzs[:50, :1]
    # ax.scatter3D(xyzs.T[0], xyzs.T[1], xyzs.T[2],color='r')

    Cx = -7
    Cy = 1.31  # almost central of the surface
    Cz = -(space[3] + space[0] * Cx + space[1] * Cy) / space[2]


    a = -60
    b = 10
    c = 0  # angle change here a,b,c parameters
    rx = np.array([[1, 0, 0, 0], [0, np.cos(a * np.pi / 180), -np.sin(a * np.pi / 180), 0],
                   [0, np.sin(a * np.pi / 180), np.cos(a * np.pi / 180), 0], [0, 0, 0, 1]])
    ry = np.array([[np.cos(b * np.pi / 180), 0, np.sin(b * np.pi / 180), 0], [0, 1, 0, 0],
                   [-np.sin(b * np.pi / 180), 0, np.cos(b * np.pi / 180), 0], [0, 0, 0, 1]])
    rz = np.array([[np.cos(c * np.pi / 180), -np.sin(c * np.pi / 180), 0, 0],
                   [np.sin(c * np.pi / 180), np.cos(c * np.pi / 180), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    r1 = rx.dot(ry)
    r = r1.dot(rz)
    t = np.array([[1, 0, 0, -Cx], [0, 1, 0, -Cy], [0, 0, 1, -Cz], [0, 0, 0, 1]])
    result = []
    for j in range(0, len(xyzs)):
        world_cor = np.array([[xyzs[j].T[0]], [xyzs[j].T[1]], [xyzs[j].T[2]], [1]])
        # print(world_cor)
        temp = r.dot(t)
        final = temp.dot(world_cor)
        result.append(final[0:3])
        ax.scatter3D(final[0], final[1], final[2], color='b')
    # result = np.array(result)
    plt.show()
    # for i in range(0,len(result)):
    #     ax.scatter3D(result[i][0], result[i][1], result[i][2],color='b')
    # plt.show()
