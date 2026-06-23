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


def sbend(wgsbend, L, H, layer_1):
    # the formula for cosine-shaped s-bend is: y(x) = H/2 * [1- cos(xpi/L)]
    # the formula for sine-shaped s-bend is: y(x) = xH/L - H/(2pi) * sin(x2*pi/L)
    def sbend(t):
        # y = H / 2 * (1 - np.cos(t * np.pi))
        y = H / 2 * (1 - np.cos(t * np.pi))
        x = L * t

        return (x, y)

    def dtsbend(t):
        dy_dt = H / 2 * np.pi * np.sin(t * np.pi)
        dx_dt = L

        return (dx_dt, dy_dt)

    wgsbend.parametric(sbend, dtsbend, number_of_evaluations=100, **layer_1)
    return wgsbend

periods = list(np.asarray(np.arange(-0.03, 0.03, 0.005)) + 0.96)
#fill_frac = 0.5
fill_factors = [0.4, 0.5,0.6]
GC_len = 60
taper_len = 30
focus_distance = GC_len + taper_len
WG_WIDTH = 2.1
position = (0, 0)
direction = "-y"
lda = 1.55
sin_theta = np.sin(np.pi * 10 / 180)
tolerance = 0.001
layer1 = 50
layer2 = 49
datatype = 0
negative = True
trench = 3*WG_WIDTH
WG_length = 1500
copies = 5
vertical_gap = 250

# Create GDS library and cell
lib = gdspy.GdsLibrary()
cell = lib.new_cell('Shai_WIFI')

# Parameters
teeth = 90
radius = 150
angle = 0.1
direction = 0
LAYER_WG = {"layer": layer1, "datatype": datatype}
LAYER_NEG = {"layer": layer2, "datatype": datatype}



y_gap= 3000

for j in range(len(fill_factors)):  # j will take values 0 and 1
    fill_frac = fill_factors[j]  # Get the fill factor based on the current index j
    print(f"Running with fill factor: {fill_frac}")
    print(f"Running with j: {j}")
    for idx, period in enumerate(periods):
        center = (0, -idx * vertical_gap-j*y_gap)
        # Call the function to create the grating path
        path1 = create_grating_path(cell, period, fill_frac, teeth, center, radius, angle, WG_WIDTH, direction,
                                    LAYER_WG={"layer": layer1, "datatype": datatype})
        path1.segment(0.5*WG_length, **LAYER_WG)
        sbend(path1, 500, 100, LAYER_WG)
        path1.segment(0.5 * WG_length, **LAYER_WG)
        cell.add(path1)
        create_grating_path(cell, period, fill_frac, teeth,
                            (path1.x + WG_WIDTH / (2 * np.tan((1 - angle) * np.pi)), path1.y), radius, angle, WG_WIDTH, 1,
                            LAYER_WG={"layer": layer1, "datatype": datatype})

        # temp1 = gdspy.boolean(cell, cell, "and")

        if negative:
            initial_angle = (1 - angle) * np.pi
            final_angle = (1 + angle) * np.pi
            arc = gdspy.Round((center[0] + trench / np.sin(angle * np.pi), center[1]),
                              radius + trench + trench / np.sin(angle * np.pi), initial_angle=initial_angle,
                              final_angle=final_angle, tolerance=0.0001, **LAYER_NEG).rotate(direction * np.pi, center)

            path_trench = gdspy.Path(WG_WIDTH + trench * 2, (center[0] - 1, center[1]))
            path_trench.segment(0.5*(WG_length + 6.5), '+x', **LAYER_NEG)
            sbend(path_trench, 500, 100, LAYER_NEG)
            path_trench.segment(0.5 * (WG_length + 6.5), '+x', **LAYER_NEG)

            arc2 = gdspy.copy(arc)
            arc2.translate(WG_length+500, 100)
            arc2.rotate(np.pi, (path1.x, path1.y))

            cell.add(arc).add(path_trench).add(arc2)


       # Add text for navigation (to track fill factors and periods)
        if idx % 2 ==0:
            text_content = f"{1000*period:.0f}"
            text_position = (center[0] + 50, center[1] + 40)  # Adjust the position for text
            text = gdspy.Text(text_content, 70, text_position)  # Added layer to text
            cell.add(text)
            text_content1 = f"{idx}"
            text_position1 = (center[0] - 290, center[1])  # Adjust the position for text
            text1 = gdspy.Text(text_content1, 70, text_position1)  # Added layer to text
            cell.add(text1)
            text_position2 = (path_trench.x + 200, path_trench.y)  # Adjust the position for text
            text2 = gdspy.Text(text_content1, 70, text_position2)  # Added layer to text
            cell.add(text2)
        if idx == 0:
            text_content = f"{fill_frac}"
            text_position = (center[1] - 900, center[0] + 200)  # Adjust the position for text
            text = gdspy.Text(text_content, 70, text_position).rotate(np.pi/2)  # Added layer to text
            cell.add(text)
            # temp2 = gdspy.boolean(cell_neg, cell_neg, "and")

            # negative_mask = gdspy.boolean(cell_neg, cell, "or")

            # cell.add(negative_mask)

    # # Plot
    # gdspy.LayoutViewer(lib)

# Write to GDS file

lib.write_gds('GC_maN_sweep_v2.gds')

# Enable running on the same kernel
gdspy.current_library = gdspy.GdsLibrary