import gdspy
import numpy as np

# Constants
WG_WIDTH = 0.7

# Layer definitions
LAYER_WG = {"layer": 174, "datatype": 0}
LAYER_SILICON_BENCH = {"layer": 123, "datatype": 0}
LAYER_SILICA = {"layer": 456, "datatype": 0}

lib = gdspy.GdsLibrary()
cell = lib.new_cell('SBS')

# parameters
center=(0,0)
radius=10
inner_radius=9.5
initial_angle=-0.2*np.pi
final_angle=0.2*np.pi
tolerance=0.0001

for i in range(10):
    arc = gdspy.Round(center, radius, inner_radius=inner_radius, initial_angle=initial_angle,
                      final_angle=final_angle, tolerance=tolerance, **LAYER_WG)
    cell.add(arc)
    radius-=1
    inner_radius-=1


# Write to GDS file
lib.write_gds('wifi.gds')
