"""
This version tries to make some loopdi'loops with parts of circles and saves then as points
Blender renders these points later (ATM with pygame)

General definitions:
    - Right is angle 0
    - Angles are ccw deined
    - Angles are in RAD
"""


# Imports
import basics
import blender

import os
import numpy as np
import random
import math
import time
import datetime as dt

import bpy
import pygame
from pygame.locals import *
print('\n')

# Global Parameters
total_planets = 3
room_width = 1200  #
room_height = 900


# Planet object that flys around
class Planet:

    def __init__(self, start_pos, start_velocity, index):
        self.index = index  # Just the number of the planet
        self.gamma = 0.5  # Gravity constant
        self.mass = 200
        self.pos = start_pos
        self.velocity = start_velocity  # V in x and y dirction
        self.force = [0, 0]  # Resulting force on Planet on x and y direction
        self.points = []
        self.bounce_factor = 0.5  # Keeps x% of velocity at bounce


    # Calc the fore
    def grav_force(self, mass1, mass2, pos1, pos2):
        angle = basics.point_angle(pos1[0], pos1[1], pos2[0], pos2[1])
        dist = basics.point_distance(pos1[0], pos1[1], pos2[0], pos2[1])

        # To prevent a mess set dist to a minimum of X
        if dist < 40:
            dist = 40

        force = (self.gamma*mass1*mass2)/(dist*dist)
        force_x, force_y = basics.angle_point(0, 0 ,angle, force)

        return [force_x, force_y]


    # Updates all the values, planets takes only the OTHER planet objects as input
    def update(self, other_planets):
        global room_width
        global room_height
        global screen

        # Get all the forces to every planet
        all_forces = []
        for x in other_planets:

            planet_f = self.grav_force(self.mass, x.mass, self.pos, x.pos)
            all_forces.append(planet_f)

        # Add forces to main force
        self.force = [0, 0]
        for f in all_forces:
            self.force[0] += f[0]
            self.force[1] += f[1]

        # Add forces to velocity
        self.velocity[0] += self.force[0]
        self.velocity[1] += self.force[1]

        # Check for bouce (With the Position in the future)
        next_pos = [self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1]]

        # Left / Right
        if next_pos[0] <= 0 or next_pos[0] >= room_width:
            self.velocity[0] *= -self.bounce_factor
            self.velocity[1] *= self.bounce_factor


        # Top / Bot
        if next_pos[1] <= 0 or next_pos[1] >= room_height:
            self.velocity[0] *= self.bounce_factor
            self.velocity[1] *= -self.bounce_factor


    # Records the current point to the points array
    def record_point(self):
        self.points.append([self.pos[0], self.pos[1]])


    # Moves the actual position
    def move(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]



    # Render function for the pygame test
    def render(self):

        if self.index == 0:
            color = (255,0,0)
        if self.index == 1:
            color = (0,0,255)
        if self.index == 2:
            color = (0,255,0)
        if self.index == 3:
            color = (180,0,230)

        pygame.draw.circle(screen, color, (self.pos[0],self.pos[1]), 30)


# Returns a full set of start variables for planets
def rand_planet_start_conditions():
    pass


# Function that does the simulation etc and saves the points
def gen_points(batches, batch_size, save_points=True, pygame_show=False):
    global screen
    global room_width
    global room_height

    # Init pygame if asked
    if pygame_show == True:
        pygame.init()
        screen = pygame.display.set_mode((room_width, room_height))

    """
    GENERATE THE POINTS WITH GRAVITY:

    This simulates Plantes with gravity and lets them fly
    If one bounces to a border it bounces back into the screen
    """

    # Array with Planet objects
    planets = []
    planets.append(Planet([100,100], [8, 1],0))
    planets.append(Planet([1000, 500], [-3, -5], 1))
    planets.append(Planet([600, 700], [-8, 1], 2))
    # planets.append(Planet([1100, 100], [-3, -4], 3))

    # Walk throug every batch and do the optins after a batch
    for batch in range(batches):

        # Time keeping
        batch_start_time = dt.datetime.now()

        # Walk through frames in a batch
        for step in range(batch_size):

            # Update the Planet values all except position (so all planets get forces from all the old positions)
            for i in range(len(planets)):

                other_planets = planets.copy()
                other_planets.pop(i)

                planets[i].update(other_planets)

            # Update and record positions
            for planet in planets:
                planet.move()
                planet.record_point()


            # Only draw pygame stuff if asked
            if pygame_show == True:

                # Render every planet
                for planet in planets:
                    planet.render()

                # Pygame stuff
                pygame.display.update()
                screen.fill((0,0,0))
                time.sleep(1/30)

                # Exit
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()


        # Extract points from the planet objects and reset recording
        batch_points = []
        for planet in planets:
            batch_points.append(planet.points)
            planet.points = []


        # Save the points to one file per batch
        if save_points == True:
            with open('points/batch_' + str(batch).rjust(3, '0') + '.points', '+w') as file:
                next_line = ''
                # Get every frame
                for f in range(len(batch_points[0])):
                    # Get every frame from every planet
                    next_line = ''
                    for p in range(len(batch_points)):
                        # Add to next line
                        next_line += str(batch_points[p][f][0]) + ',' + str(batch_points[p][f][1]) + ';'

                    file.write(next_line + '\n')

                # Close file after using it
                file.close()

        # Print batch message
        batch_end_time = dt.datetime.now()
        batch_time_delta = batch_end_time - batch_start_time
        print('Batch ' + str(batch) + ' completed in: ' + str(batch_time_delta))



# Main function
def main():
    gen_points(200, 50000, save_points=True, pygame_show=False)
    blender.prepare()


# Run Main
if __name__ == "__main__":
    main()
