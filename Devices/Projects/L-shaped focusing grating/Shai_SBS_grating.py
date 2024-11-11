# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 11:15:46 2024

@author: benamis9
"""

import numpy as np
import gdspy
from grating import create_grating_path 

periods         = list(np.asarray(np.arange(-0.02, 0.025, 0.005)) + 0.558)
fill_frac       = 0.5
GC_len          = 60
taper_len       = 30
focus_distance  = GC_len + taper_len
WG_WIDTH        = 0.7
position        = (0,0)
direction       = "-y"
lda             = 1.55
sin_theta       = np.sin(np.pi * 10 / 180)
tolerance       = 0.001
layer1          = 50
layer2          = 49
datatype        = 0
negative        = True
trench          = 2
WG_length       = 7000
copies          = 5
vertical_gap    = 500


# Create GDS library and cell
lib = gdspy.GdsLibrary()
cell        = lib.new_cell('Shai_WIFI')
cell_neg    = lib.new_cell('Shai_WIFI_negative')
cell_final  = lib.new_cell('Shai_WIFI_final')

# Parameters
teeth = 90
radius = 90
angle = 0.1
direction = 0
LAYER_WG  = {"layer": layer1, "datatype": datatype}
LAYER_NEG = {"layer": layer2, "datatype": datatype}

for idx, period in enumerate(periods):
    center = (0, -idx*vertical_gap)
    # Call the function to create the grating path
    path1 = create_grating_path(cell, period, fill_frac, teeth, center, radius, angle, WG_WIDTH, direction, LAYER_WG={"layer": layer1, "datatype": datatype})
    path1.segment(WG_length, **LAYER_WG)
    cell.add(path1)
    create_grating_path(cell, period, fill_frac, teeth, (path1.x + WG_WIDTH / (2*np.tan((1 - angle) * np.pi)), path1.y), radius, angle,WG_WIDTH, 1, LAYER_WG={"layer": layer1, "datatype": datatype})
    
    # temp1 = gdspy.boolean(cell, cell, "and")
    
    if negative:
        initial_angle = (1 - angle) * np.pi
        final_angle   = (1 + angle) * np.pi
        arc = gdspy.Round((center[0]+trench/np.sin(angle*np.pi), center[1]), radius + trench + trench/np.sin(angle*np.pi),  initial_angle=initial_angle, final_angle=final_angle, tolerance=0.0001, **LAYER_NEG).rotate(direction*np.pi, center)
        
        path_trench = gdspy.Path(WG_WIDTH + trench*2, (center[0]-1, center[1]))
        path_trench.segment(WG_length+6.5, '+x', **LAYER_NEG)
        
        arc2 = gdspy.copy(arc)
        arc2.translate(WG_length, 0)
        arc2.rotate(np.pi, (path1.x, path1.y))
        
        cell_neg.add(arc).add(path_trench).add(arc2)
        
        # temp2 = gdspy.boolean(cell_neg, cell_neg, "and")
        
        # negative_mask = gdspy.boolean(temp2, temp1, "not")
        
        # cell_final.add(negative_mask)

# Plot
gdspy.LayoutViewer(lib)

# Write to GDS file
lib.write_gds('Shai_SBS.gds')

# Enable running on the same kernel
gdspy.current_library = gdspy.GdsLibrary()


