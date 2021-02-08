import bpy


# General
scene = bpy.data.scenes["Scene"]


planets = []

# Create and add keyframe settings
for i in range(3):
    bpy.ops.mesh.primitive_ico_sphere_add()
    planets.append(bpy.context.active_object)
    planets[i]

# Set point for any frame
for frame in range(30):
    for planet in planets:
        
        # Change location
        planet.location = [frame/10, frame/10, frame/10]
        
        # Add keyframeg
        planet.keyframe_insert(data_path="location", frame=frame)



# Render and render settings
scene.render.filepath = '/home/gresse/PythonProjects/GravityAnimation/test'
scene.render.image_settings.file_format = "AVI_RAW"
bpy.ops.render.view_show()
bpy.ops.render.render(animation=True)

