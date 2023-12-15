from re import M
import bpy
import random
from mathutils import Vector
from math import radians, cos, sin, pi
import json

# Constants
SPHERE_COLOR = (0, 0.6, 1, 1)
EMISSION_STRENGTH = 10
NUMBER_OF_SPHERES = 10
LARGER_SPHERE_RADIUS = 3
SMALLER_SPHERE_RADIUS = 0.05
FRAME_START = 1
FRAME_END = 1000
HORIZONTAL_ANGLE_RANGE = 300
DURATION_START = 400
DURATION_END = 700
CUT_FIRST_PERCENTAGE_OF_ANIMATION = 0.3
INVISIBLE_CYCLES = 2
MIN_DISTANCE = 2
MAX_DISTANCE = 2.5
FILE_PATH = "./animation.usdz"
MATERIALS_FILE_PATH = "./materials.json"
BACKGROUND_COLOR = (0, 0, 0, 1)
VOLUMNE_DENSITY = 0.015
VOLUME_ANISOTROPY = 0.05
LIGHT_LOCATION = (0, 0, MAX_DISTANCE * 1.5)
LIGHT_ENERGY = 1000
LIGHT_COLOR = (1, 1, 1)


# New function to save materials to a separate JSON file
def save_materials_to_json(materials, file_path=MATERIALS_FILE_PATH):
    """
    Save materials to a JSON file for dynamic modification in the iOS app.

    Parameters:
    file_path (str): Path to save the JSON file.
    materials (dict): Dictionary of material properties.
    """
    with open(file_path, "w") as outfile:
        json.dump(materials, outfile, indent=4)


def create_sphere(location, radius, color, emission_strength, materials_dict):
    """
    Create a UV sphere at a specified location with given properties.

    Parameters:
    location (Vector): The location to place the sphere.
    radius (float): Radius of the sphere.
    color (tuple): RGBA color for the sphere's material.
    emission_strength (float): Emission strength of the sphere's material.
    """
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)
    sphere = bpy.context.object

    # Create a new material and set it to use nodes
    mat = bpy.data.materials.new(name="EmissiveMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Clear existing nodes
    nodes.clear()

    # Create an Emission node and set its properties
    emission = nodes.new(type="ShaderNodeEmission")
    emission.inputs["Color"].default_value = [
        color[0],
        color[1],
        color[2],
        1,
    ]  # RGB and Alpha
    emission.inputs["Strength"].default_value = emission_strength

    # Create a Material Output node and connect Emission to it
    material_output = nodes.new(type="ShaderNodeOutputMaterial")
    mat.node_tree.links.new(
        emission.outputs["Emission"], material_output.inputs["Surface"]
    )

    # Assign the material to the sphere
    sphere.data.materials.append(mat)

    materials_dict[sphere.name] = {
        "color": color,
        "emission_strength": emission_strength,
    }
    return sphere


def animate_visibility(
    sphere, frame_start, frame_end, cycles, emission_strength, exclude_sphere_name
):
    """
    Animate the visibility of a sphere, making it repeatedly transition between visible and invisible states.

    Parameters:
    sphere (Object): The Blender object (sphere) to which the visibility animation will be applied.

    frame_start (int): The frame number where the visibility animation begins. This sets the starting point
                       for the visibility changes in the animation timeline.

    frame_end (int): The frame number where the visibility animation ends. This sets the endpoint for the
                     visibility changes in the animation timeline.

    cycles (int, optional): The number of visibility cycles (invisible-to-visible-to-invisible) the sphere
                            will undergo during the animation. Defaults to 4 if not specified.

    Functionality:
    - The function divides the total animation duration (from 'frame_start' to 'frame_end') into equal parts
      based on the number of cycles.
    - For each cycle, it randomly determines a point within that cycle's time frame to transition the sphere
      from invisible to visible, and another point to transition back to invisible.
    - Keyframes are inserted at these points to animate the visibility state changes.

    Usage:
    - This function is used to create a dynamic effect where the sphere appears and disappears at various
      intervals during the animation.
    - It enhances the visual complexity and interest of the animation by introducing random visibility changes.

    Note:
    - The 'hide_viewport' and 'hide_render' properties of the sphere are used to control its visibility in
      the Blender viewport and in the final render, respectively.
    - Adjusting the 'cycles' parameter can increase or decrease the frequency of the visibility changes.
    """
    if sphere.name == exclude_sphere_name:
        sphere.hide_viewport = True
        sphere.hide_render = True
        return
    duration = frame_end - frame_start
    cycle_length = duration // cycles
    emission_increase_duration = int(
        0.2 * bpy.context.scene.render.fps
    )  # Duration for increased emission in frames

    for i in range(cycles):
        cycle_start = frame_start + i * cycle_length
        cycle_end = cycle_start + cycle_length

        # Random points within the cycle for visibility change
        start_visible = random.randint(cycle_start, cycle_end - 1)
        end_visible = random.randint(start_visible + 1, cycle_end)

        # Initial state - invisible
        sphere.hide_viewport = True
        sphere.hide_render = True
        sphere.keyframe_insert(data_path="hide_viewport", frame=cycle_start)
        sphere.keyframe_insert(data_path="hide_render", frame=cycle_start)

        # Ensure material exists and has an Emission node
        if not sphere.data.materials:
            # Create a new material if none exists
            mat = bpy.data.materials.new(name="SphereMat")
            mat.use_nodes = True
            sphere.data.materials.append(mat)
        else:
            mat = sphere.data.materials[0]

        if "Emission" not in mat.node_tree.nodes:
            # Add an Emission node if it doesn't exist
            emission_node = mat.node_tree.nodes.new(type="ShaderNodeEmission")
            mat.node_tree.links.new(
                mat.node_tree.nodes["Material Output"].inputs["Surface"],
                emission_node.outputs["Emission"],
            )
        else:
            emission_node = mat.node_tree.nodes["Emission"]

        # Animate to visible with increased emission
        sphere.hide_viewport = False
        sphere.hide_render = False
        emission_node.inputs["Strength"].default_value = emission_strength * 3
        sphere.keyframe_insert(data_path="hide_viewport", frame=start_visible)
        sphere.keyframe_insert(data_path="hide_render", frame=start_visible)
        emission_node.inputs["Strength"].keyframe_insert(
            "default_value", frame=start_visible
        )

        # Animate emission back to original after 0.2 seconds
        emission_node.inputs["Strength"].default_value = emission_strength
        emission_node.inputs["Strength"].keyframe_insert(
            "default_value", frame=start_visible + emission_increase_duration
        )

        # Animate back to invisible
        sphere.hide_viewport = True
        sphere.hide_render = True
        sphere.keyframe_insert(data_path="hide_viewport", frame=end_visible)
        sphere.keyframe_insert(data_path="hide_render", frame=end_visible)
        # Smooth transition for visibility
        for fcurve in sphere.animation_data.action.fcurves:
            if fcurve.data_path in ["hide_viewport", "hide_render"]:
                for keyframe in fcurve.keyframe_points:
                    keyframe.interpolation = "CONSTANT"


def animate_orbit(
    sphere,
    center,
    duration,
    frame_start,
    frame_end,
    horizontal_angle_range,
    reverse=False,
):
    """
    Animate a sphere in a horizontal orbit around a center point.

    Parameters:
    sphere (Object): The sphere to be animated.
    center (Object): The center point around which the sphere orbits.
    duration (float): Total duration of the orbit in frames.
    frame_start (int): Starting frame of the animation.
    frame_end (int): Ending frame of the animation.
    horizontal_angle_range (float): Range of the horizontal angle in degrees.
    """
    frame_count = frame_end - frame_start
    orbit_radius = (sphere.location - center.location).length
    z_value = center.location.z

    for frame in range(frame_count):
        bpy.context.scene.frame_set(frame_start + frame)
        phase = (frame / duration) * horizontal_angle_range
        if reverse:
            phase = -phase
        angle = radians(phase)
        x = cos(angle) * orbit_radius
        y = sin(angle) * orbit_radius
        sphere.location = Vector((x, y, z_value))
        sphere.keyframe_insert(data_path="location", frame=(frame_start + frame))
        # Ensure smooth interpolation
        for fcurve in sphere.animation_data.action.fcurves:
            for keyframe in fcurve.keyframe_points:
                keyframe.interpolation = "BEZIER"


def create_all_spheres(
    number_of_spheres,
    min_distance,
    max_distance,
    smaller_sphere_radius,
    color,
    emission_strength,
):
    """
    Create multiple spheres at random positions within a specified distance range from a central point.

    Parameters:
    number_of_spheres (int): The number of small spheres to create. These spheres are distributed around
                             a central point within a specified distance range.

    min_distance (float): The minimum distance from the central point at which a small sphere can be placed.
                          This sets the lower bound for the distance range within which spheres will be created.

    max_distance (float): The maximum distance from the central point at which a small sphere can be placed.
                          This sets the upper bound for the distance range within which spheres will be created.

    smaller_sphere_radius (float): The radius of each small sphere. This parameter determines the size of
                                   the spheres that are created.

    color (tuple): The RGBA color value for the spheres. This color will be applied to all the spheres created.

    emission_strength (float): The emission strength of the spheres' material. This parameter affects how
                               brightly the spheres appear in the rendered animation.

    Functionality:
    - The function randomly positions each sphere at a distance from a central point. This distance is randomly
      chosen within the range specified by 'min_distance' and 'max_distance'.
    - For each sphere, spherical coordinates (theta and phi) are converted to Cartesian coordinates (x, y, z)
      to determine its position in 3D space.
    - Each sphere is then created at its calculated position with the specified color and emission strength.

    Usage:
    - This function is used to populate a 3D space with spheres distributed around a central point,
      creating a visually dynamic scene.
    - It allows for variability in the positioning of spheres, enhancing the complexity and appeal of the scene.

    Note:
    - Adjusting 'min_distance' and 'max_distance' changes the spread of the spheres around the central point,
      affecting the overall look of the scene.
    - The 'smaller_sphere_radius' parameter can be used to control the size of the individual spheres.
    """
    materials = {}
    for _ in range(number_of_spheres):
        theta = random.uniform(0, 2 * pi)
        phi = random.uniform(0, pi)

        distance = random.uniform(min_distance, max_distance)

        x = distance * sin(phi) * cos(theta)
        y = distance * sin(phi) * sin(theta)
        z = distance * cos(phi)
        location = Vector((x, y, z))
        create_sphere(
            location, smaller_sphere_radius, color, emission_strength, materials
        )

        location_1a = Vector((-x, -y, -z))
        create_sphere(
            location_1a, smaller_sphere_radius, color, emission_strength, materials
        )

        radius_1b = (distance + distance / 2) / 2
        x_1b = radius_1b * sin(phi) * cos(theta)
        y_1b = radius_1b * sin(phi) * sin(theta)
        z_1b = radius_1b * cos(phi)
        location_1b = Vector((x_1b, y_1b, z_1b))
        create_sphere(
            location_1b, smaller_sphere_radius, color, emission_strength, materials
        )

        location_1c = Vector((-x_1b, -y_1b, -z_1b))
        create_sphere(
            location_1c, smaller_sphere_radius, color, emission_strength, materials
        )

        # Additional sphere with different attributes
        additional_radius = random.uniform(
            SMALLER_SPHERE_RADIUS / 2, SMALLER_SPHERE_RADIUS * 1.5
        )
        additional_location = Vector((-x, -y, -z))
        create_sphere(
            additional_location, additional_radius, color, emission_strength, materials
        )
    save_materials_to_json(materials)


def setup_camera(max_distance):
    # Assuming the center of your animation is at (0, 0, 0)
    center_of_animation = (0, 0, max_distance * 2)

    # Create a new camera
    bpy.ops.object.camera_add(location=center_of_animation)
    camera = bpy.context.object

    # Rotate the camera to look straight down
    # camera.rotation_euler[0] = radians(90)

    # Set the camera's lens type to orthographic and adjust the orthographic scale
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = max_distance * 2  # Adjust this value as needed


def create_point_light(location, energy, color):
    """
    Create a point light at a specified location.

    Parameters:
    location (tuple): The location to place the light.
    energy (float): The intensity of the light.
    color (tuple): The color of the light.
    """
    bpy.ops.object.light_add(type="POINT", location=location)
    light = bpy.context.object
    light.data.energy = energy
    light.data.color = color
    return light


def setup_world_volume_scatter(density, anisotropy):
    # Access the world settings
    world = bpy.data.worlds[
        "World"
    ]  # Replace 'World' with your world's name if different

    # Use nodes for the world
    world.use_nodes = True
    nodes = world.node_tree.nodes

    # Clear existing nodes
    nodes.clear()

    # Create a new Volume Scatter node
    volume_scatter = nodes.new(type="ShaderNodeVolumeScatter")
    volume_scatter.inputs["Density"].default_value = density
    volume_scatter.inputs["Anisotropy"].default_value = anisotropy

    # Create a new Background node
    background = nodes.new(type="ShaderNodeBackground")

    # Create a Volume node
    volume = nodes.new("ShaderNodeVolumeAbsorption")

    # Create an Add Shader node
    add_shader = nodes.new(type="ShaderNodeAddShader")

    # Link the nodes
    links = world.node_tree.links
    links.new(volume.outputs[0], add_shader.inputs[0])
    links.new(volume_scatter.outputs[0], add_shader.inputs[1])
    # Ensure 'World Output' node is present
    world_output = nodes.get("World Output")
    if not world_output:
        world_output = nodes.new(type="ShaderNodeOutputWorld")
    links.new(add_shader.outputs[0], world_output.inputs["Surface"])


def add_volume_emission_to_spheres(color, emission_strength):
    for obj in bpy.data.objects:
        # Create a new material with volume emission
        mat = bpy.data.materials.new(name=f"{obj.name}_VolumeEmission")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes

        # Clear existing nodes
        nodes.clear()

        material_output = nodes.new(type="ShaderNodeOutputMaterial")

        # Create an Emission node
        emission = nodes.new(type="ShaderNodeEmission")
        emission.inputs["Color"].default_value = color
        emission.inputs["Strength"].default_value = emission_strength

        # Create a Volume Scatter node
        volume_scatter = nodes.new(type="ShaderNodeVolumeScatter")
        volume_scatter.inputs["Density"].default_value = 0.015
        volume_scatter.inputs["Anisotropy"].default_value = 0.05

        # Create an Add Shader node
        add_shader = nodes.new(type="ShaderNodeAddShader")

        # Link the nodes
        links = mat.node_tree.links
        links.new(emission.outputs[0], add_shader.inputs[0])
        links.new(volume_scatter.outputs[0], add_shader.inputs[1])
        links.new(add_shader.outputs[0], material_output.inputs["Volume"])

        # Assign the material to the sphere
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)


def create_3d_model(
    number_of_spheres,
    larger_sphere_radius,
    min_distance,
    max_distance,
    smaller_sphere_radius,
    frame_start,
    frame_end,
    horizontal_angle_range,
    sphere_color,
    emission_strength,
    duration_start,
    duration_end,
    cut_first_percentage_of_animation,
    invisible_cycles,
    file_path,
    background_color,
    volume_density,
    volume_anisotropy,
    light_location,
    light_energy,
    light_color,
):
    """
    Create the entire 3D model and animations in Blender.

    Parameters:
    number_of_spheres (int): The total number of small spheres to be created. These spheres are distributed  evenly around the larger sphere.

    larger_sphere_radius (float): The radius of the larger, central sphere.

    min_distance (float): The minimum distance from the center of the larger central sphere at which a small  sphere can be placed. This value sets the lower bound of the orbit radius for the  small spheres. Increasing this value will ensure that all small spheres are placed  at least this distance away from the center.

    max_distance (float): The maximum distance from the center of the larger central sphere at which a small sphere can be placed. This value sets the upper bound of the orbit radius for the small spheres. Decreasing this value will ensure that no small sphere is placed beyond this distance from the center.

    smaller_sphere_radius (float): The radius of each smaller sphere that orbits around the larger sphere.  Adjusting this value changes the size of these orbiting spheres.

    frame_start (int): The starting frame number for the animation. This sets the beginning point of the animation  timeline. The animation will start from this frame.

    frame_end (int): The ending frame number for the animation. This sets the endpoint of the animation timeline. The animation will end at this frame.

    horizontal_angle_range (float): The range of the horizontal angle in degrees for the orbiting motion of the  spheres. This determines how far around the central sphere the smaller spheres  will orbit.

    sphere_color (tuple): The RGBA color value for the smaller spheres. This color will be applied to all smaller  spheres in the animation.

    emission_strength (float): The emission strength of the sphere's material. This value affects the brightness  of the sphere's color in the rendered animation.

    duration_start (float): The minimum duration (in frames) of the orbit for each small sphere. This value  sets the lower limit for the random speed selection of each sphere's orbit.

    duration_end (float): The maximum duration (in frames) of the orbit for each small sphere. This value  sets the upper limit for the random speed selection of each sphere's orbit.

    cut_first_percentage_of_animation (float): The percentage of the initial part of the animation to cut.  This value should be between 0 and 1. For example, a value of 0.2  will cut the first 20% of the animation.

    invisible_cycles (int): The number of cycles each sphere goes through in its visibility animation  (invisible to visible and back). This determines how many times each sphere  will appear and disappear during the animation.

    file_path (str): file path where to save the .usdz file
    Note:
    - The animation is created by first generating the spheres, then applying orbit and visibility animations.
    - The animation timeline can be adjusted by changing 'frame_start' and 'frame_end'.
    - The orbit speed and pattern can be varied by adjusting 'duration_start', 'duration_end', and
      'horizontal_angle_range'.
    - The appearance of spheres is controlled by 'sphere_color', 'emission_strength', and 'invisible_cycles'.
    - To trim the animation, adjust 'cut_first_percentage_of_animation'.
    """
    # Clear existing objects

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[
        "Color"
    ].default_value = background_color
    # setup_world_volume_scatter(volume_density, volume_anisotropy)

    # Create central invisible sphere
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=larger_sphere_radius, location=(0, 0, 0)
    )
    central_sphere = bpy.context.object
    central_sphere.hide_render = True
    large_sphere_name = central_sphere.name

    create_all_spheres(
        number_of_spheres,
        min_distance,
        max_distance,
        smaller_sphere_radius,
        sphere_color,
        emission_strength,
    )
    # Call the function with your color and emission strength
    # add_volume_emission_to_spheres(sphere_color, emission_strength)
    for sphere in bpy.data.objects:
        if "Sphere" in sphere.name:
            duration = random.uniform(duration_start, duration_end)
            reverse_orbit = random.choice([True, False])
            animate_orbit(
                sphere,
                central_sphere,
                duration,
                frame_start,
                frame_end,
                horizontal_angle_range,
                reverse=reverse_orbit,
            )
            animate_visibility(
                sphere,
                frame_start,
                frame_end,
                invisible_cycles,
                emission_strength,
                large_sphere_name,
            )
    # Calculate new start frame (cutting the first 20% of the animation)
    total_frames = frame_end - frame_start
    new_frame_start = frame_start + int(
        total_frames * cut_first_percentage_of_animation
    )
    bpy.data.objects.remove(bpy.data.objects[large_sphere_name], do_unlink=True)

    create_point_light(light_location, light_energy, light_color)
    setup_camera(max_distance)

    # Update scene's frame start and end
    bpy.context.scene.frame_start = new_frame_start
    bpy.context.scene.frame_end = frame_end
    bpy.ops.wm.usd_export(
        filepath=file_path,
        check_existing=False,
        filter_blender=False,
        filter_backup=False,
        export_animation=True,
        export_hair=True,
        export_uvmaps=True,
        filter_volume=True,
    )


create_3d_model(
    sphere_color=SPHERE_COLOR,
    emission_strength=EMISSION_STRENGTH,
    larger_sphere_radius=LARGER_SPHERE_RADIUS,
    min_distance=MIN_DISTANCE,
    max_distance=MAX_DISTANCE,
    smaller_sphere_radius=SMALLER_SPHERE_RADIUS,
    number_of_spheres=NUMBER_OF_SPHERES,
    frame_start=FRAME_START,
    frame_end=FRAME_END,
    horizontal_angle_range=HORIZONTAL_ANGLE_RANGE,
    duration_start=DURATION_START,
    duration_end=DURATION_END,
    cut_first_percentage_of_animation=CUT_FIRST_PERCENTAGE_OF_ANIMATION,
    invisible_cycles=INVISIBLE_CYCLES,
    file_path=FILE_PATH,
    background_color=BACKGROUND_COLOR,
    volume_density=VOLUMNE_DENSITY,
    volume_anisotropy=VOLUME_ANISOTROPY,
    light_location=LIGHT_LOCATION,
    light_energy=LIGHT_ENERGY,
    light_color=LIGHT_COLOR,
)
