# "C:/Program Files/Blender Foundation/Blender 3.6/python/bin/python.exe" your_script.py

# "C:\Program Files\Blender Foundation\Blender 4.3\4.3\python\bin\python.exe"

import bpy
import os
import mathutils
import sys
import math

def load_texture(image_path):
    # Check if the image is already loaded in Blender
    image_name = os.path.basename(image_path)
    if image_name in bpy.data.images:
        return bpy.data.images[image_name]
    
    # Load the image and return it
    image = bpy.data.images.load(image_path)
    return image

def apply_texture_to_material(material, texture_image_path):
    if material.use_nodes:
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        # Clear existing nodes
        nodes.clear()

        # Load the image here to ensure it's fresh and stays in memory
        texture_image = bpy.data.images.load(texture_image_path)
        
        # Optionally pack the image to keep it in memory
        texture_image.pack()

        # Create a new Image Texture node and assign the texture
        texture_node = nodes.new(type='ShaderNodeTexImage')
        texture_node.image = texture_image

        # Create a Principled BSDF shader node
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')

        # Create an Output Material node
        output_node = nodes.new(type='ShaderNodeOutputMaterial')

        # Link nodes
        links.new(texture_node.outputs['Color'], bsdf_node.inputs['Base Color'])
        links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])

        # Adjust material properties for less glare
        if 'Specular' in bsdf_node.inputs:
            bsdf_node.inputs['Specular'].default_value = 0.2
        if 'Roughness' in bsdf_node.inputs:
            bsdf_node.inputs['Roughness'].default_value = 0.8

        # Print to verify texture application
        print(f"Applied texture: {texture_image.filepath} to material: {material.name}")
    else:
        # Ensure the material uses nodes
        material.use_nodes = True
        apply_texture_to_material(material, texture_image_path)


def ensure_uv_map(obj):
    if not obj.data.uv_layers:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.uv.smart_project()
        bpy.ops.object.mode_set(mode='OBJECT')

def render_thumbnail(input_filepath, output_filepath, texture_image_path=None, rotation=(0, 0, 0)):
    # Clear existing objects
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # Check the file extension and use appropriate import operator
    if input_filepath.lower().endswith('.obj'):
        bpy.ops.import_scene.obj(filepath=input_filepath)  # Import OBJ
    elif input_filepath.lower().endswith('.fbx'):
        bpy.ops.import_scene.fbx(filepath=input_filepath)  # Import FBX
    else:
        raise ValueError("Unsupported file format")
    
    # Ensure there are objects in the scene after import
    if not bpy.context.selected_objects:
        raise RuntimeError("Import failed or no objects found")
    
    # Set up camera
    bpy.ops.object.camera_add(location=(5, -5, 1))  # Adjust as necessary
    camera = bpy.context.object
    bpy.context.scene.camera = camera

    # Set the camera to look at the origin (0, 0, 0)
    direction = mathutils.Vector((0, 0, 0)) - camera.location
    rot_quat = direction.to_track_quat('Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Select all objects (imported model)
    imported_object = None
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            obj.select_set(True)
            imported_object = obj

    if imported_object is None:
        raise RuntimeError("No mesh objects found")

    # Ensure the object has a UV map
    ensure_uv_map(imported_object)

    # Apply rotation to the imported object
    imported_object.rotation_euler = (
        math.radians(rotation[0]),
        math.radians(rotation[1]),
        math.radians(rotation[2])
    )

    # Apply texture if provided
    if texture_image_path:
        for material_slot in imported_object.material_slots:
            apply_texture_to_material(material_slot.material, texture_image_path)
    
    # Calculate the bounding box to center the view on the model
    bpy.ops.view3d.camera_to_view_selected()
    
    # Set up improved lighting
    # Key light
    bpy.ops.object.light_add(type='AREA', location=(5, -5, 5))
    key_light = bpy.context.object
    key_light.data.energy = 2500
    key_light.data.size = 4
    key_light.data.spread = 1.0  # Use spread to soften the shadows
    key_light.data.shadow_soft_size = 1.0  # Increase shadow softness

    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(-5, -5, 5))
    fill_light = bpy.context.object
    fill_light.data.energy = 2000
    fill_light.data.size = 4
    fill_light.data.spread = 1.0  # Use spread to soften the shadows
    fill_light.data.shadow_soft_size = 1.0  # Increase shadow softness

    # Back light
    bpy.ops.object.light_add(type='AREA', location=(0, 5, 5))
    back_light = bpy.context.object
    back_light.data.energy = 1500
    back_light.data.size = 4
    back_light.data.spread = 1.0  # Use spread to soften the shadows
    back_light.data.shadow_soft_size = 1.0  # Increase shadow softness

    # Environment light (ambient light)
    if bpy.context.scene.world is None:
        bpy.context.scene.world = bpy.data.worlds.new("World")
    bpy.context.scene.world.use_nodes = True
    env_node_tree = bpy.context.scene.world.node_tree
    env_bg = env_node_tree.nodes.new(type='ShaderNodeBackground')
    env_bg.inputs[1].default_value = 0.75  # Adjust the strength of the environment light
    env_output = env_node_tree.nodes.get('World Output')
    env_node_tree.links.new(env_bg.outputs[0], env_output.inputs[0])

    # Set render settings
    bpy.context.scene.render.filepath = output_filepath
    bpy.context.scene.render.engine = 'CYCLES'  # Use Cycles renderer for better lighting
    bpy.context.scene.cycles.samples = 100  # Adjust samples for better quality
    bpy.context.scene.render.resolution_x = 512
    bpy.context.scene.render.resolution_y = 512
    bpy.context.scene.render.film_transparent = True
    
    # Render the scene
    bpy.ops.render.render(write_still=True)


def batch_render_thumbnails(directory_path, single_texture=None):

    # Load the single texture if provided
    print(f"Loading single texture: {single_texture}")
    texture_image = None
    if single_texture:
        texture_image = load_texture(single_texture)
        print(f"Using single texture: {single_texture}")

    asset_dir = os.path.join(directory_path, "assets")
    print(f"Rendering thumbnails for FBX files in: {asset_dir}")

    for file in os.listdir(asset_dir):
        if file.lower().endswith('.fbx'):
            if not single_texture:
                # Load a texture image for each FBX file
                texture_image_path = os.path.join(asset_dir, file.replace('.FBX', '.PNG'))
            else:
                texture_image_path = single_texture
            
            input_filepath = os.path.join(asset_dir, file)
            output_filename = file.lower().replace('.fbx', '_thumbnail.png')
            output_dir = os.path.join(directory_path, "output")
            output_filepath = os.path.join(output_dir, output_filename)
            
            # Render thumbnail
            # -45, 0, 45 for plants
            # 
            render_thumbnail(input_filepath, output_filepath, texture_image_path=texture_image_path, rotation=(-22, 15, 90))

# Example usage
if __name__ == "__main__":
    # debug argv
    print(sys.argv)
    print(len(sys.argv))

    for i in range(len(sys.argv)):
        print(f"sys.argv[{i}] = {sys.argv[i]}")

    if len(sys.argv) > 5:
        directory_path = sys.argv[5]  # Take the second last argument as the directory path
    else:
        directory_path = input("Please enter the directory path: ")

    single_texture = None
    if len(sys.argv) > 6:
        single_texture = sys.argv[6]  # Take the last argument as the single texture path
    
    if not os.path.isdir(directory_path):
        print(f"From Render.Py - Error: {directory_path} is not a valid directory.")
    else:
        batch_render_thumbnails(directory_path, single_texture if single_texture else None)
