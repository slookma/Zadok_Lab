import numpy as np
import gdspy

def create_grating_path(cell, priodicity, fill_factor, grating_period, center, radius, angle, WG_WIDTH,
                        direction, LAYER_WG={"layer": 174, "datatype": 0}):
    """

    :param cell: cell writing file on
    :param priodicity: what is the size of the period
    :param fill_factor: how much of the period is full
    :param grating_period: how many teeth do we want
    :param center: center of the circle we are drawing around (where in the X Y plane is the grating)
    :param radius: radius of the whole WIFI coupler
    :param angle: in rad (example 0.5 = 90 degrees on each side = half a circle)
    :param WG_WIDTH: the width of the WG wanted at the end
    :param direction: 0 for "+x" ; 1 for "+y" ; 2 for "-x" ; 3 for "-y"
    :param LAYER_WG: layer
    :return: the path - can be continued for element
    """

    # Calculate inner radius and angles
    inner_radius = radius - priodicity * fill_factor
    initial_angle = (1 - angle) * np.pi
    final_angle = (1 + angle) * np.pi


    # Create grating arcs
    for _ in range(grating_period):
        arc = gdspy.Round(center, radius, inner_radius=inner_radius, initial_angle=initial_angle,
                          final_angle=final_angle, tolerance=0.0001, **LAYER_WG)
        cell.add(arc)
        radius -= priodicity
        inner_radius -= priodicity

    # Create slice and waveguide path
    arc = gdspy.Round(center, radius,  initial_angle=initial_angle,
                          final_angle=final_angle, tolerance=0.0001, **LAYER_WG)
    arc_slice = gdspy.slice(arc, [center[0] - WG_WIDTH / (2*np.tan(initial_angle)),
                                  center[0] + WG_WIDTH / (2*np.tan(initial_angle))], axis=0, **LAYER_WG)

    waveguide_path = gdspy.Path(WG_WIDTH, (center[0] + WG_WIDTH / (2*np.tan(initial_angle)), center[1]))

    cell.add(arc_slice[0]).add(waveguide_path)
    
    # 1. Rotate Polygons (PolygonSet objects)
    for poly in cell.polygons:
        poly.rotate(direction*np.pi/2, center)

    # 2. Rotate Paths (FlexPath / RobustPath objects)
    for path in cell.paths:
        path.rotate(direction*np.pi/2, center)

    return waveguide_path
