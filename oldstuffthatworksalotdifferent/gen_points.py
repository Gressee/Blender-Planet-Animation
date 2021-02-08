"""
This are the old methonds of gnerating a path
"""



# Genereate the points that belong to a partial circle
def gen_circle_points(start_x, start_y, last_angle):
    """
    DOES NOT WORK ATM

    The start values is thee point the last circle rendered
    The start angle is the direction the next circle has to start on
    Then a radius is randomly decided on
    Then the fraction of the circle is randomly decided on
    The center pos of the circle ha an angle of +- pi/4 relative to the start_angle
    and the radius as distance.

    Differentiate between absolute dirctions of the circle Tangente and the angle
    between the center point and the draw point
    """

    # Generate random values
    radius = 100#random.randint(50, 300)
    rot_dir = 'cw'#random.choice(['cw', 'ccw'])

    if rot_dir == 'cw':
        center_angle = basics.clamp_angle(last_angle + math.pi/2)   # Angle from start to center point
        circle_angle = math.pi/2#random.uniform(-0.2, -4)
        start_angle = basics.clamp_angle(last_angle + math.pi/2)
        end_angle = basics.clamp_angle(start_angle - circle_angle)

    if rot_dir == 'ccw':
        center_angle = basics.clamp_angle(last_angle - math.pi/2)   # Angle from start to center point
        circle_angle = math.pi#random.uniform(0.2, 4)
        start_angle = basics.clamp_angle(last_angle  - math.pi/2)
        end_angle = basics.clamp_angle(start_angle + circle_angle)

    # Get center of circle
    center_x = start_x + round(radius * math.cos(center_angle))
    center_y = start_y + round(radius * math.sin(center_angle))


    # Calc new points get stored in a 2d array
    points = []
    angle = basics.clamp_angle(start_angle)
    angle_step = 0.001 # How much the angle increases every move

    print('\nDir: ', rot_dir)
    print('Last Angle: ', last_angle)
    print('Start Angle: ', start_angle)
    print('Center Pos: ' + str(center_x) + '  ' + str(center_y))
    print('Center Angle: ', center_angle)
    print('Angle: ', angle)
    print('End Angle: ', end_angle)
    print()

    while (abs(end_angle-angle) > angle_step):

        # Add new points to array
        x = center_x + round(radius * math.cos(angle))
        y = center_y + round(radius * math.sin(angle))

        # Check if x,y is already the last entry in the points array else append
        if not points == []:
            if not points[-1] == [x,y]:
                points.append([x,y])
        else:
            points.append([x,y])

        # Increase angle
        if rot_dir == 'cw':
            angle -= angle_step
        if rot_dir == 'ccw':
            angle += angle_step

        angle = basics.clamp_angle(angle)

    # Calc the last dir of the tangente
    if rot_dir == 'cw':
        next_last_angle = angle - math.pi/2
    if rot_dir == 'ccw':
        next_last_angle = angle + math.pi/2

    # Return points
    return [points, next_last_angle]


# Generate the points with a circle rotate arond other circles etc..
def gen_points(main_center_x, main_center_y, arms, steps, max_angle):

    """
    This works that there is a main center, around that a point rotates in a circle.
    This around this point another point rotates and around that another, etc...
    The positions of the last rotating point are the generated points
    """

    # Set arrays
    points = []
    rads = []
    angles = []
    speed = []  # Angle is plus that every step
    center_pos = [[main_center_x, main_center_y]]

    for i in range(arms):

        # Set random values
        rads.append(random.randint(10, 200))
        angles.append(random.uniform(0, math.pi*2))
        speed.append(random.uniform(-max_angle, max_angle))

        # Calc the center positions (there are one more centers than arms bc the last center doesnt has an arm)
        x = center_pos[i-1][0] + round(rads[i] * math.cos(angles[i]))
        y = center_pos[i-1][1] + round(rads[i] * math.sin(angles[i]))
        center_pos.append([x,y])


    # Simulate the stuff
    for step in range(steps):
        for i in range(arms):
            center_pos[i+1][0] = round(center_pos[i][0] + rads[i] * math.cos(angles[i]))
            center_pos[i+1][1] = round(center_pos[i][1] + rads[i] * math.sin(angles[i]))
            angles[i] += speed[i]

        points.append([center_pos[-1][0], center_pos[-1][1]])

    # Return the points
    print('Generated ' + str(steps) + ' Points')
    return points
