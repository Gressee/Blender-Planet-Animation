# Imports
import basics
import bpy


# General Blender variables
objects = bpy.data.objects # Even if defined at start if its called it returns all the objs that exist ATM


def create_planets():
    objs = []
    for i in range(total_planets):

        # Create object
        bpy.ops.mesh.primitive_ico_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        # Get the obj from the created planet
        p = bpy.context.active_object
        # Rename the obj
        p.name = "Planet" + str(i)
        # Add to list
        objs.append(p)


def set_planet_keyframes(planets, points_file):

    # Read points array from file
    points = []
    with open('points/batch_000.points', 'r') as file:
        string = file.read()

        # Close file after using
        file.close()

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
    # Set keyframes
    for i in range(len(points)):
        for i in range(len(points[i])):

            # Move to frame
            bpy.context.scene.frame_current = i

            # Set new location for planet
            planet[j].loacation = [points[i][j][0], points[i][j][1], 0]  # Planest move in x-y-Plane

            # Add the keyframe
            planet[j].keyframe_insert()


def set_camera_settings(camera):

    # Pos and Rot
    camera.location = [0, 0, 5]
    camera.rotation_euler = [0, 90, 0]


def set_light_settings(light):
    light.data.type = 'SUN'
    bpy.context.object.data.energy = 2


def set_render_settings():
    global frames

    # Set frames
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_step = 1
    bpy.context.scene.frame_end = frames


    # Quality settings
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.cycles.samples = 32


def render_animation():


    # Output
    bpy.data.scenes["Scene"].render.fps = 30
    bpy.data.scenes["Scene"].render.filepath = '/home/gresse/PythonProjects/GravityAnimation/test'
    bpy.data.scenes["Scene"].render.image_settings.file_format = "AVI_RAW"

    # Render
    bpy.ops.render.render(animation=True)


# Prepare the blender file (sort of a main function)
def prepare():

    # Get camera and light constant
    for obj in objects:
        if obj.name == "Camera":
            camera = obj
        if obj.name == "Light":
            light = obj


    # Make file settings
    set_camera_settings(camera)
    set_light_settings(light)
    set_render_settings()

    # Create the Planets
    planets = create_planets()

    # Set the keyframes
    set_planet_keyframes(planets, 'points/batch_000.points')
