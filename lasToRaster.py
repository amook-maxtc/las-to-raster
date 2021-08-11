import numpy as np
import pylas
import cv2
import math
import networkx as nx


def sigmoid(x):
    return 1/(1+math.exp(-0.7 * x))


def edge_weight(target, home, matrix):
    return np.abs(matrix[target] - matrix[home])


las = pylas.read("./color.laz", 'r')
print(las)
i = 0
points = las.points
r = 512
d = np.empty([r,r],dtype=object)
for i in range(0,r):
    for j in range(0,r):
        d[i,j] = []
        # print("x: {}, y: {}".format(i,j));
imageMatrix = np.zeros([r,r,3])
# print(d[0,0])
# print(type(d[226,255]))
Xmin = points[0][0]
Xmax = points[0][0]
Ymin = points[0][1]
Ymax = points[0][1]

average = 0
num = 0
min = points[0][2]
max = points[0][2]
print(points[0])
for point in points:
    x, y, z = point[0], point[1], point[2]
    average += z if (num == 0) else (z/(num))
    average *= 1 if (num == 0) else (num)/(num+1.0)
    num += 1
    if (z > max):
        max = z
    elif (z < min):
        min = z
    if (x < Xmin):
        Xmin = x
    elif (x > Xmax):
        Xmax = x

    if (y < Ymin):
        Ymin = y
    elif (y > Ymax):
        Ymax = y
print(average)
print(max)
print(min)
print(max-average)

print("Min: ({},{}), Max: ({},{})".format(Xmin, Ymin, Xmax, Ymax))
variance = 0
num_points = 0
xDiv = (Xmax-Xmin)/r + 1
yDiv = (Ymax-Ymin)/r + 1
for point in points:
    i += 1
    num_points += 1
    x, y, z = point[0], point[1], point[2]
    xIndex = int((x-Xmin)//xDiv)
    yIndex = int((y-Ymin)//yDiv)
    # print("x: {}, y: {} | {}".format(xIndex, yIndex, type(d[xIndex,yIndex])));
    d[xIndex, yIndex].append(z)
    # variance += (z - average) ** 2
    # print("Point ({}) | x: {}, y: {}, z: {}".format(i,x,y,z))

average_matrix = np.zeros((r, r), dtype='f')

for idx, element in np.ndenumerate(d):
    if len(element) > 0:
        element = np.mean(element)
        average_matrix[idx] = element
    else:
        average_matrix[idx] = np.NINF  # numpy negative infinity

print(average_matrix, '\n')

i_input_home = int(input('Input the x-coordinate of the starting node: '))
j_input_home = int(input('Input the y-coordinate of the starting node: '))
print('(', + i_input_home, ',', + j_input_home, ') is the starting node.')

i_input_destination = int(input('Input the x-coordinate of the ending node: '))
j_input_destination = int(input('Input the y-coordinate of the ending node: '))
print('(', + i_input_destination, ',', + j_input_destination, ') is the ending node.')

print('\n')

raster_graph = nx.grid_2d_graph(5, 5)

for idx2, element2 in np.ndenumerate(average_matrix):
    raster_graph.add_node(average_matrix[idx2])

for index, value in np.ndenumerate(average_matrix):
    u = index
    for u, v, d in raster_graph.edges(data=True):
        d['weight'] = edge_weight(u, v, average_matrix)
    print(raster_graph.adj[index].items())

short = nx.shortest_path(raster_graph, (i_input_home, j_input_home), (i_input_destination, j_input_destination))
print(short)
