# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 11:15:46 2024

@author: benamis9
"""

import numpy as np
import gdspy
from grating import create_grating_path 
import sys
sys.path.insert(0, '../Consortium')
from s_bend_func import sbendPath, sbendPathM

periods         = list(np.asarray(np.arange(-0.02, 0.025, 0.005)) + 0.540)
fill_fracs      = list([0.5, 0.6])
WG_WIDTH        = 0.7
layer1          = 50
layer2          = 49
datatype        = 0
trench_path     = 2
trench_sector   = 6
WG_length       = 7000
vertical_gap    = 200


# Create GDS library and cell
lib  = gdspy.GdsLibrary()
cell = lib.new_cell('Shai_WIFI')

# Parameters
teeth = 90
radius = 90
angle = 0.12
direction = 0
LAYER_WG  = {"layer": layer1, "datatype": datatype}
LAYER_NEG = {"layer": layer2, "datatype": datatype}

for idx_DC, fill_frac in enumerate(fill_fracs):
    for idx_per, period in enumerate(periods):
        center = (0, -(idx_per + idx_DC*len(periods))*vertical_gap)
    
        initial_angle = (1 - angle) * np.pi
        final_angle   = (1 + angle) * np.pi
        arc = gdspy.Round((center[0]+trench_path/np.sin(angle*np.pi), center[1]), radius + trench_path + trench_sector/np.sin(angle*np.pi),  initial_angle=initial_angle, final_angle=final_angle, tolerance=0.0001, **LAYER_NEG).rotate(direction*np.pi, center)
        
        path_trench = gdspy.Path(trench_path, (center[0]-1, center[1]))
        path_trench.segment(WG_length/2, '+x', **LAYER_NEG)
        sbendPath(path_trench, 1000, 100, LAYER_NEG)
        path_trench.segment(WG_length/2 - 1000 + 6.5, '+x', **LAYER_NEG)
        
        arc2 = gdspy.copy(arc)
        arc2.translate(WG_length + 13.42, 100)
        arc2.rotate(np.pi, (path_trench.x, path_trench.y))
        
        cell.add(arc).add(path_trench).add(arc2)

# Plot
gdspy.LayoutViewer(lib)

# Write to GDS file
lib.write_gds('Shai_SBS_CrEtch.gds')

# Enable running on the same kernel
gdspy.current_library = gdspy.GdsLibrary()




