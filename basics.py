"""
Script with the absolute basic python/math/geometry functions
"""

import math

# Point distance
def point_distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))


# Angle from pos1 to pos2 in rads (right is 0, ccw is positive)
def point_angle(x1, y1, x2, y2):
    dist_x = x2-x1
    dist_y = y2-y1

    # Return if no angle
    if dist_x == 0 and dist_y == 0:
            return 0

    # Cases if x1 != x2
    if dist_x > 0 and dist_y >= 0:
        angle = math.pi*2 - math.atan(dist_y/dist_x)

    if dist_x < 0 and dist_y >= 0:
        angle = math.pi + math.atan(dist_y/-dist_x)

    if dist_x < 0 and dist_y <= 0:
        angle = math.pi - math.atan(-dist_y/-dist_x)

    if dist_x > 0 and dist_y <= 0:
        angle = math.atan(-dist_y/dist_x)

    # Special cases for x1 = x2
    if dist_x == 0 and dist_y < 0:
        angle = math.pi/2

    if dist_x == 0 and dist_y > 0:
        angle = math.pi + math.pi/2

    return angle


# Point from a given angle in RAD with a radius
def angle_point(x, y, angle, radius):

    angle = clamp_angle(angle)
    point = []

    # Cases for the angle
    if angle >= 0 and angle <= math.pi/2:
        point = [math.cos(angle)*radius + x, -math.sin(angle)*radius + y]

        return point


    if angle >= math.pi/2 and angle <= (math.pi):
        angle = math.pi - angle
        point = [-math.cos(angle)*radius + x, -math.sin(angle)*radius + y]

        return point


    if angle >= math.pi and angle <= 1.5*math.pi:
        angle -= math.pi
        point = [-math.cos(angle)*radius + x, math.sin(angle)*radius + y]

        return point


    if angle >= 1.5*math.pi and angle <= 2*(math.pi):
        angle = 2*math.pi - angle
        point = [math.cos(angle)*radius + x, math.sin(angle)*radius + y]

        return point


    return point


# Clamp
def clamp(number, min, max):
    if number <= min:
        number = min
    if number >= max:
        number = max
    return number


# Clamp angle between 0 and 2pi
def clamp_angle(angle):
    while (angle < 0 or angle > 2*math.pi):
        if angle < 0:
            angle += math.pi*2
        if angle > 2*math.pi:
            angle -= 2*math.pi

    return angle


# Convert Deg to Rad
def deg_to_rad(a):
    return (a/360) * 2*math.pi
