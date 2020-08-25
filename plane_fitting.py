import numpy as np
from ransac import *
import euclidtransform

def augment(xyzs):
    axyz = np.ones((len(xyzs), 4)) # row = len(xyzs), column = 4
    axyz[:, :3] = xyzs
    return axyz

def estimate(xyzs):
    axyz = augment(xyzs[:3])
    return np.linalg.svd(axyz)[-1][-1, :]

def is_inlier(coeffs, xyz, threshold):
    return np.abs(coeffs.dot(augment([xyz]).T)) < threshold

if __name__ == '__main__':
    import matplotlib
    import matplotlib.pyplot as plt
    from mpl_toolkits import mplot3d
    fig = plt.figure()
    ax = mplot3d.Axes3D(fig)

    def plot_plane(a, b, c, d):
        xx, yy = np.mgrid[-20:20, -20:30]
        return xx, yy, (-d - a * xx - b * yy) / c # aX+bY+cZ+d = 0 平面方程

    n = 108770
    max_iterations = 6000
    goal_inliers = n * 0.70

    # test data
    file = open('points3Dchange.txt')
    xyzs=[]
    for line in file.readlines():
        curLine=line.strip().split(' ')
        floatLine=list(map(float,curLine)) #这里使用的是map函数直接把数据转化成为float类型
        xyzs.append(floatLine[1:4])
    # print('dataMat:',dataMat)

    xyzs=np.array(xyzs)
    # print('!!!!',xyzs)
    # xyzs[:50, 2:] = xyzs[:50, :1]
    ax.scatter3D(xyzs.T[0], xyzs.T[1], xyzs.T[2],color='r')
    # plt.show()

    # RANSAC
    m, b = run_ransac(xyzs, estimate, lambda x, y: is_inlier(x, y, 0.01), 3, goal_inliers, max_iterations)
    a, b, c, d = m
    # print('???',m)
    xx, yy, zz = plot_plane(a, b, c, d)
    # print('!!!',xx,yy,zz)
    ax.plot_surface(xx, yy, zz, color= '#ADEAEA') #石板蓝色 easier when observing

    plt.show()

    euclidTransform.euclidTrans(xyzs, m)

