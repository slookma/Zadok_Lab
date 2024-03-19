import gdspy
import numpy as np


def create_grating_path(cell, priodicity, fill_factor, grating_period, center, radius, angle, WG_WIDTH, direction, LAYER_WG={"layer": 174, "datatype": 0}):
    """

    :param cell: cell writing file on
    :param priodicity: what is the size of the period
    :param fill_factor: how much of the period is full
    :param grating_period: how many teeth do we want
    :param center: center of the circle we are drawing around (where in the X Y plane is the grating)
    :param radius: radius of the whole WIFI coupler
    :param angle: in rad (example 0.5 = 90 degrees on each side = half a circle)
    :param WG_WIDTH: the width of the WG wanted at the end
    :param direction: 0 for "+x" 1 for "-x". assuming the device is writen in the "+x" direction
    :param LAYER_WG: layer
    :return: the path - can be continued for element
    """

    # Calculate inner radius and angles
    inner_radius = radius - priodicity * fill_factor
    initial_angle = (1 - angle) * np.pi
    final_angle = (1 + angle) * np.pi

    # Manually specify slice
    slice_idx = 2 if direction else 0

    # Create grating arcs
    for _ in range(grating_period):
        arc = gdspy.Round(center, radius, inner_radius=inner_radius, initial_angle=initial_angle,
                          final_angle=final_angle, tolerance=0.0001, **LAYER_WG)
        arc = arc.rotate(direction * np.pi, center)
        cell.add(arc)
        radius -= priodicity
        inner_radius -= priodicity

    # Create slice and waveguide path
    arc = gdspy.Round(center, radius,  initial_angle=initial_angle,
                          final_angle=final_angle, tolerance=0.0001, **LAYER_WG).rotate(direction*np.pi, center)
    arc_slice = gdspy.slice(arc, [center[0] - WG_WIDTH / (2*np.tan(initial_angle)),
                                  center[0] + WG_WIDTH / (2*np.tan(initial_angle))], axis=0, **LAYER_WG)

    waveguide_path = gdspy.Path(WG_WIDTH, (center[0] + WG_WIDTH / (2*np.tan(initial_angle)), center[1]))

    cell.add(arc_slice[slice_idx]).add(waveguide_path)

    return waveguide_path

# example

# Create GDS library and cell
lib = gdspy.GdsLibrary()
cell = lib.new_cell('WIFI')

# Parameters
priodicity = 1
fill_factor = 0.2
grating_period = 5
center = (0, 0)
radius = 10
angle = 0.1
WG_WIDTH = 0.7
direction = 0
LAYER_WG = {"layer": 174, "datatype": 0}

# Call the function to create the grating path
path1 = create_grating_path(cell, priodicity, fill_factor, grating_period, center, radius, angle, WG_WIDTH, direction)
path1.segment(10, **LAYER_WG)
cell.add(path1)
create_grating_path(cell, priodicity,fill_factor,grating_period,(path1.x + WG_WIDTH / (2*np.tan((1 - angle) * np.pi)), path1.y), radius, angle,WG_WIDTH, 1)
# Write to GDS file
lib.write_gds('wifi.gds')
