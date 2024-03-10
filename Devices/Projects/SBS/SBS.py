import gdspy
import numpy as np

def create_path(width, length, start_point, layer):
    path = gdspy.Path(width, start_point)
    path.segment(length, **layer)
    return path

# Constants
WG_WIDTH = 0.7
SILICA_WIDTH = 1.3
SBS_LENGTH = 140
SILICA_LENGTH = 180

# Layer definitions
LAYER_WG = {"layer": 174, "datatype": 0}
LAYER_SILICON_BENCH = {"layer": 123, "datatype": 0}
LAYER_SILICA = {"layer": 456, "datatype": 0}

# Starting points
START_POINT_WG = (0, 0)
START_POINT_SILICA = (-20, 0)

# Create GDS library and cell
lib = gdspy.GdsLibrary()
cell = lib.new_cell('SBS')

# Create waveguide path
wg_path = create_path(WG_WIDTH, SBS_LENGTH, START_POINT_WG, LAYER_WG)

# Create Silicon-on-insulator (SOI) path
soi_path = create_path(SILICA_WIDTH, SILICA_LENGTH, START_POINT_SILICA, LAYER_SILICON_BENCH)

# Create Silica path
silica_path = create_path(SILICA_WIDTH, SILICA_LENGTH, START_POINT_SILICA, LAYER_SILICA)

# Add paths to the cell
cell.add(wg_path).add(soi_path).add(silica_path)

# Write to GDS file
lib.write_gds('SBS.gds')
