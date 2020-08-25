import numpy as np
from collections import Counter

import matplotlib.pyplot as plt


class imageData:
    # vertices and edges
    numpts = None
    pts = {}

    # Graph Constructor
    def __init__(self, numpts):
        self.pts = {}
        for i in range(numpts):
            self.pts.setdefault(i, []).append('')

    def createPts(self, num: int, pts: list, idx: int):
        # norm
        pts = pts / pts[2, 0]
        # for pts
        self.pts[idx].append(pts)

        if self.pts[idx][0] == '':
            self.pts[idx].pop(0)


def quat2rotm(quat):
    q = quat.copy()
    npversion_q = np.array(q)
    m = np.size(npversion_q, 0)
    n = np.size(npversion_q, 1)
    matrix = []
    for i in range(0, m):  # rows
        rot_matrix = np.array(
            [[1.0 - 2.0 * float(npversion_q[i, 2]) * float(npversion_q[i, 2]) - 2.0 * float(npversion_q[i, 3]) * float(
                npversion_q[i, 3]),
              2.0 * float(npversion_q[i, 1]) * float(npversion_q[i, 2]) + 2.0 * float(npversion_q[i, 0]) * float(
                  npversion_q[i, 3]),
              2.0 * float(npversion_q[i, 1]) * float(npversion_q[i, 3]) - 2.0 * float(npversion_q[i, 0]) * float(
                  npversion_q[i, 2])],
             [2.0 * float(npversion_q[i, 1]) * float(npversion_q[i, 2]) - 2.0 * float(npversion_q[i, 0]) * float(
                 npversion_q[i, 3]),
              1.0 - 2.0 * float(npversion_q[i, 1]) * float(npversion_q[i, 1]) - 2.0 * float(npversion_q[i, 3]) * float(
                  npversion_q[i, 3]),
              2.0 * float(npversion_q[i, 2]) * float(npversion_q[i, 3]) + 2.0 * float(npversion_q[i, 0]) * float(
                  npversion_q[i, 1])],
             [2.0 * float(npversion_q[i, 1]) * float(npversion_q[i, 3]) + 2.0 * float(npversion_q[i, 0]) * float(
                 npversion_q[i, 2]),
              2.0 * float(npversion_q[i, 2]) * float(npversion_q[i, 3]) - 2.0 * float(npversion_q[i, 0]) * float(
                  npversion_q[i, 1]),
              1.0 - 2.0 * float(npversion_q[i, 1]) * float(npversion_q[i, 1]) - 2.0 * float(npversion_q[i, 2]) * float(
                  npversion_q[i, 2])]],
            dtype=q.dtype)
        matrix.append(rot_matrix)
    return matrix


with open('images.txt', 'r') as f1, open('images_change.txt', 'w') as f2:
    for line in f1.readlines():
        line = line.strip()
        if "JPG" in line:
            f2.write(line + '\n')
file = open('images_change.txt')
images_change = []
for line in file.readlines():
    curLine = line.strip().split(' ')
    floatLine = list(curLine)
    images_change.append(floatLine[1:8])
images_change = np.array(images_change)
# print(images_change[:,4])
file_handle = open('rotationmatrix.txt', mode='w')
file_handle.writelines(str(quat2rotm(images_change)))

# camera stuffs
with open('cameras.txt', 'r') as f1, open('cameras_change.txt',
                                          'w') as f2:  # read the camera parameters, save in camera_change.txt
    for line in f1.readlines():
        line = line.strip()
        if "SIMPLE_RADIAL" in line:  # we only have one camera here therefore finding simple radial.
            f2.write(line + '\n')
file = open('cameras_change.txt')
camera_change = []
for line in file.readlines():
    curLine = line.strip().split(' ')
    floatLine = list(curLine)
    camera_change.append(floatLine[2:7])
camera_change = np.array(camera_change)
# print(camera_change)
# film plane to pixels * perspective projection
width = float(camera_change[0, 0])
height = float(camera_change[0, 1])
focal_length = float(camera_change[0, 2])
principle_pointx = float(camera_change[0, 3])
principle_pointy = float(camera_change[0, 4])
matrix_temp = np.array(
    [[focal_length / width, 0, principle_pointx, 0], [0, focal_length / height, principle_pointy, 0], [0, 0, 1, 0]])
# print(matrix_temp)

# world to camera
numofrows = np.size(quat2rotm(images_change), 0)
# b = np.zeros((1,3*108))
# padding_rotation = np.row_stack(quat2rotm(images_change),b)
# print(padding_rotation)
rotation_matrix = quat2rotm(images_change)
# print(rotation_matrix[107])
padding_matrix = [0, 0, 0]
rotation_matrix_final = []
for j in range(0, numofrows):
    new_rotation_matrix = np.row_stack((rotation_matrix[j], padding_matrix))
    rotation_matrix_final.append(new_rotation_matrix)
# print(rotation_matrix_final)

Tx = images_change[:, 4]
Ty = images_change[:, 5]
Tz = images_change[:, 6]

T_final = []
for j in range(0, numofrows):
    T_final_temp = np.array([[Tx[j]], [Ty[j]], [Tz[j]], [1]])
    T_final.append(T_final_temp)

worldtocameramatrix = []
for j in range(0, numofrows):
    worldtocameramatrix_temp = np.hstack((rotation_matrix_final[j], T_final[j]))
    worldtocameramatrix.append(worldtocameramatrix_temp)
worldtocameramatrix = np.array(worldtocameramatrix, dtype=np.float)

# final stage of pinhole camera model
pixellocation_final = []
for j in range(0, numofrows):
    pixellocation_temp = np.dot(matrix_temp, worldtocameramatrix[j])
    pixellocation_final.append(pixellocation_temp)
pixellocation_final = np.array(pixellocation_final, dtype=np.float)
# print(pixellocation_final[0])

# 3d camera location and camera matrix
file = open('points3Dchange.txt')  # prabably saving problem above
points3Dandnumber = []
for line in file.readlines():
    curLine = line.strip().split(' ')
    floatLine = list(map(float, curLine))
    points3Dandnumber.append(floatLine[1:9])
# points3Dandnumber = np.array(points3Dandnumber)
sumpixels = np.size(points3Dandnumber, 0)
points3Dandnumber = np.array(points3Dandnumber, dtype=np.float)
# print(points3Dandnumber)
# print(points3Dandnumber[1,:])

# memo2dset_final =[[] for i in range(numofrows)]
memo2dset_finalx = np.zeros((numofrows + 1, sumpixels))
memo2dset_finaly = np.zeros((numofrows + 1, sumpixels))
memo2dset_finalz = np.zeros((numofrows + 1, sumpixels))

a = points3Dandnumber[:, -1].copy()
# print(int(a[108768])) #successfully turn the value into int form from 0-108769 success for kitchen image.

# print(pixellocation_final[-1])
imagepts = imageData(numofrows)

for j in range(numofrows):
    for i in range(sumpixels):
        if int(a[i]) == j + 1:
            worldpoint = [[points3Dandnumber[i, 0]], [points3Dandnumber[i, 1]], [points3Dandnumber[i, 2]], [1]]
            memo2dset_temp = np.dot(pixellocation_final[j], worldpoint)
            # print(memo2dset_temp)
            imagepts.createPts(numofrows, memo2dset_temp, j)
        else:
            continue

print(imagepts)

for i in range(numofrows):

    plt.figure('Draw')
    ptsx = []
    ptsy = []
    for j in range(len(imagepts.pts[i])):
        if imagepts.pts[i] != '':
            ptsx.append(imagepts.pts[i][j][0, 0])
            ptsy.append(imagepts.pts[i][j][1, 0])
    plt.scatter(ptsx, ptsy, alpha=0.6)  # point colors
    # plt.show() # SIMPLY SAVE AT LOCAL FILE

    plt.savefig("easyplot" + str(i + 1) + ".jpg")  # 保存图象

    plt.close()  # close the plots
