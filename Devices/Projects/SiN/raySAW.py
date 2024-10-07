import gdspy
import numpy as np

# Initialize GDS library and create a new cell
lib = gdspy.GdsLibrary()
cell = lib.new_cell('waveguide_grating_ring_array_xy_shift')

# Define waveguide, ring, and grating parameters
wg_width = 1.0  # Waveguide width
taper_length = 150.0  # Taper length in µm
taper_width = 0.2  # Final width of the taper
ring_radius = 100.0  # Ring radius in µm
ring_straight_length = 60.0  # Length of the straight segment inside the ring
grating_width = 1.0  # Width of each grating stripe in µm
grating_empty_space = 1.0  # Empty space between grating stripes in µm
grating_area_size = 60.0  # Grating area size (60 µm x 60 µm)
layer_wg = {"layer": 174, "datatype": 0}  # Waveguide and ring layer
grat_ring_dis = 5  # Horizontal displacement between grating and ring
x_grating_start = 200.0  # Initial x-axis position of the grating
segment_length = x_grating_start + grating_area_size  # Length of the waveguide segment
chip_size = 5000

# Define the step size for shifting in both x and y directions
y_offset_step = 30  # Y-axis offset for each new structure
x_offset_step = 320  # X-axis offset for each new structure (same as y_offset)

# change as wanted
initial_ring_dis = 0.8  # Starting vertical displacement between waveguide and ring
ring_dis_increment = 0.05  # Increment of 0.5 µm for each new structure
layer_grating = {"layer": 150, "datatype": 0}  # Grating layer - CHANGE TO RIGHT LAYER

# Function to create a taper (inverse taper or normal taper based on 'out')
def taper(path, layer, taper_length=150.0, taper_width=0.2, out=0):
    if out:
        path.segment(taper_length, final_width=taper_width, **layer)
    else:
        path.segment(taper_length, final_width=wg_width, **layer)

# Function to create a ring centered at (x, y)
def ring(x, y, layer, radius=100.0, straight_length=60.0):
    ring_path = gdspy.Path(wg_width, (x, y))
    ring_path.turn(radius=radius, angle=np.pi / 2, **layer) \
        .segment(straight_length, **layer) \
        .turn(radius=radius, angle=np.pi, **layer) \
        .segment(straight_length, **layer) \
        .turn(radius=radius, angle=np.pi / 2, **layer)
    cell.add(ring_path)

# Function to create a grating in a 60 µm x 60 µm area
def grating(x, y, layer, width=1.0, empty_space=1.0, size=60.0):
    current_x = x
    while current_x < x + size:
        stripe = gdspy.Rectangle((current_x, y), (current_x + width, y + size), **layer)
        cell.add(stripe)
        current_x += width + empty_space

# Create multiple waveguide-grating-ring structures with both x-axis and y-axis offsets
ring_dis = initial_ring_dis  # Initialize ring_dis
for i in range(13):  # Number of structures to create
    y_offset = -i * y_offset_step  # Calculate the y-axis shift for each structure
    x_offset = i * x_offset_step  # Calculate the x-axis shift for each structure

    # Create the waveguide path starting at (x_offset, y_offset)
    wg_path = gdspy.Path(taper_width, (0, y_offset))
    y_start = wg_path.y

    # Add inverse taper at the beginning (widening to wg_width)
    taper(wg_path, layer_wg, taper_length=taper_length, taper_width=taper_width, out=0)

    # Add the straight waveguide segment
    wg_path.segment(x_offset + segment_length + ring_radius, **layer_wg).turn(ring_radius, np.pi / 2, **layer_wg) \
        .segment(ring_straight_length, **layer_wg).turn(ring_radius, -np.pi / 2, **layer_wg) \
        .segment(chip_size - wg_path.x - taper_length, **layer_wg)

    # Add inverse taper at the end (narrowing to taper_width)
    taper(wg_path, layer_wg, taper_length=taper_length, taper_width=taper_width, out=1)

    # Add the waveguide path to the cell
    cell.add(wg_path)

    # Grating Placement Position
    x_grating_pos = x_grating_start + x_offset + ring_radius  # Shift the x position of the grating
    h_grating = wg_width + ring_radius  # y-axis height of the grating

    # Create the grating at the calculated position
    grating(x_grating_pos, h_grating + y_start, layer_grating, width=grating_width, empty_space=grating_empty_space,
            size=grating_area_size)

    # Ring Placement Position
    x_ring_pos = x_grating_pos + grating_area_size + grat_ring_dis + ring_radius  # Adjust x position for the ring
    y_ring = y_start + ring_dis + wg_width  # y-axis: away from the waveguide with increasing `ring_dis`

    # Create the ring at the specified position
    ring(x_ring_pos, y_ring, layer_wg, radius=ring_radius, straight_length=ring_straight_length)

    # Update ring_dis for the next structure
    ring_dis += ring_dis_increment

# Write the GDS file
lib.write_gds('waveguide_grating_ring_array_xy_shift.gds')

print("GDS file 'waveguide_grating_ring_array_xy_shift.gds' has been created successfully.")
