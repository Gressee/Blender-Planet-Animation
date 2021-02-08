import math
import basics
import numpy as np
import os
import time
import sys


points = []
with open('points/batch_000.points', 'r') as file:
    string = file.read()

    # Split into lines (one frame is one line)
    points = string.split('\n')

    # Split into differen sets of coordinates
    for i in range(len(points)):
        points[i] = points[i].split(';')

    # Split the set of coordinates into 2 values
    for i in range(len(points)):
        for j in range(len(points[i])):
            points[i][j] = points[i][j].split(',')

    print(points)
    # Convert into float
    for i in range(len(points)):
        for i in range(len(points[i])):
            for k in range(len(points[i][j])):
                # points[i][j][k] = points[i][j][k].replace('\n', '')
                # points[i][j][k] = points[i][j][k].replace(';', '')
                # points[i][j][k] = points[i][j][k].replace(',', '')
                points[i][j][k] = float(points[i][j][k])

print(points)
