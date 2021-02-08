"""
This file contains all the draw functions to draw to
an image array
"""

import basics
import numpy as np


# Circle
def circle(array, center_x, center_y, radius, color):

    """
    Loops through every point in square around around circle and Check
    if point is in circle
    """

    # Get array dim
    array_dim = array.shape

    # square borders
    right = int(basics.clamp(center_x + radius, 0, array_dim[1]-1))
    left = int(basics.clamp(center_x - radius, 0, array_dim[1]-1))
    top = int(basics.clamp(center_y - radius, 0, array_dim[0]-1))
    bot = int(basics.clamp(center_y + radius, 0, array_dim[0]-1))

    for x in range(left, right+1):
        for y in range(top, bot+1):
            dist = basics.point_distance(center_x, center_y, x, y)
            if dist <= radius:
                array[y][x] = color

    return array
