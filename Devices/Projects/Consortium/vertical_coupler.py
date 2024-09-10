import gdspy
import numpy as np

# # gds specifications
# gds starting
lib = gdspy.GdsLibrary()
# layer
layer_linbo = {"layer": 174, "datatype": 0}
layer_sin = {"layer": 175, "datatype": 0}
# cell
cell1 = lib.new_cell('vertical_coupler')
dy = 5
radios = 50
theta = np.arccos(1-dy/(2*radios))
lc = 120
path_linbo = gdspy.Path(0.25)
path_sin = gdspy.Path(0.347, (0, dy))

path_sin.turn(0, -theta, **layer_sin).turn(radios, theta, **layer_sin).segment(lc, **layer_sin).turn(radios, theta, **layer_sin)
path_linbo.turn(0, theta, **layer_linbo).turn(radios, -theta, **layer_linbo).segment(lc, **layer_linbo).turn(radios, -theta, **layer_linbo)

cell1.add(path_linbo).add(path_sin)

lib.write_gds('vertical_coupler.gds')