import gdspy
import numpy as np

# # gds specifications
# layer
layer_linbo = {"layer": 174, "datatype": 0}
layer_sin   = {"layer": 175, "datatype": 0}
overwrite   = 1
dy          = 10    # [um]
radius      = 500   # [um]
lc          = 120   # [um]
l_start     = 1     # [um]
theta       = np.arccos(1-dy/(4*radius))
path_linbo  = gdspy.Path(0.25)
path_sin    = gdspy.Path(0.347, (0, dy))

# gds starting
lib = gdspy.GdsLibrary()
# cell
cell1 = lib.new_cell('vertical_coupler')

path_sin.segment(l_start, **layer_sin).turn(radius, -theta, **layer_sin).turn(radius, theta, **layer_sin).segment(lc, **layer_sin).turn(radius, theta, **layer_sin).turn(radius, -theta, **layer_sin).segment(l_start, **layer_sin)
path_linbo.segment(l_start, **layer_linbo).turn(radius, theta, **layer_linbo).turn(radius, -theta, **layer_linbo).segment(lc, **layer_linbo).turn(radius, -theta, **layer_linbo).turn(radius, theta, **layer_linbo).segment(l_start, **layer_linbo)

cell1.add(path_linbo).add(path_sin)
    
if overwrite == 0:
    lib.write_gds("vertical_coupler_Lc" + str(lc) + "um.gds")

gdspy.LayoutViewer(lib)
gdspy.current_library = gdspy.GdsLibrary()