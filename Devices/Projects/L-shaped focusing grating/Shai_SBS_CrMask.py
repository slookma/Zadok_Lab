# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 11:31:47 2024

@author: benamis9
"""

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

overwrite       = 0 # 0 - Don't write GDS, 1 - Write GDS
periods         = list(np.asarray(np.arange(-0.02, 0.025, 0.005)) + 0.550)
fill_fracs      = list([0.5])
layer1          = 50
layer2          = 49
datatype        = 0
trench_path     = 2
trench_sector   = 6
WG_length       = 6000
vertical_gap    = 200
L_coups         = list([5,6,7,8])
gap_coup        = 0.2
WG_WIDTH        = 0.7
R               = 200

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

initial_angle = (1 - angle) * np.pi
final_angle   = (1 + angle) * np.pi

for idx_DC, fill_frac in enumerate(fill_fracs):
    for idx_per, period in enumerate(periods):
        center = (0, -(idx_per + idx_DC*len(periods))*vertical_gap)
        
        arc = gdspy.Round((center[0]+trench_sector/np.sin(angle*np.pi), center[1]), radius + trench_sector + trench_sector/np.sin(angle*np.pi),  initial_angle=initial_angle, final_angle=final_angle, tolerance=0.0001, **LAYER_NEG).rotate(direction*np.pi, center)
        
        path_trench = gdspy.Path(trench_path, (center[0]-1, center[1]))
        path_trench.segment(WG_length/2 - 500, '+x', **LAYER_NEG)
        sbendPath(path_trench, 1000, 100, LAYER_NEG)
        path_trench.segment(WG_length/2 - 500 + 6.5, '+x', **LAYER_NEG)
        
        arc2 = gdspy.copy(arc)
        arc2.translate(WG_length, 100)
        arc2.rotate(np.pi, (path_trench.x, path_trench.y))
        
        cell.add(arc).add(path_trench).add(arc2)

# Add Rings
for idx_rings, L_coup in enumerate(L_coups):
    center = (0, -(len(periods)*len(fill_fracs)+1)*vertical_gap - idx_rings*vertical_gap - R)
    
    arc = gdspy.Round((center[0]+trench_sector/np.sin(angle*np.pi), center[1]), radius + trench_sector + trench_sector/np.sin(angle*np.pi),  initial_angle=initial_angle, final_angle=final_angle, tolerance=0.0001, **LAYER_NEG).rotate(direction*np.pi, center)
    
    path_trench = gdspy.Path(trench_path, (center[0]-1, center[1]))
    path_trench.segment(600 + idx_rings*(2*R+L_coup+100), **LAYER_NEG)
    x_ring = path_trench.x - 100
    y_ring = path_trench.y + gap_coup + WG_WIDTH
    path_trench.turn(R, 'l', **LAYER_NEG)
    path_trench.turn(R, 'r', **LAYER_NEG)
    path_trench.segment(300 + (len(L_coups)-idx_rings-1)*(2*R+L_coup+100), **LAYER_NEG)
    
    ring1_trench = gdspy.Path(trench_path, (x_ring, y_ring))
    ring1_trench.segment(L_coup, **LAYER_NEG)
    ring1_trench.turn(R, 'll', **LAYER_NEG)
    ring1_trench.segment(L_coup, **LAYER_NEG)
    ring1_trench.turn(R, 'll', **LAYER_NEG)

    arc2 = gdspy.copy(arc)
    arc2.rotate(np.pi, (center[0], center[1]))
    arc2.translate(path_trench.x, 2*R)
    
    cell.add(arc).add(path_trench).add(ring1_trench).add(arc2)
    
    
for idx_rings, L_coup in enumerate(L_coups):
    center = (3200, -(len(periods)*len(fill_fracs)+1)*vertical_gap - idx_rings*vertical_gap - R)
    
    arc = gdspy.Round((center[0]+trench_sector/np.sin(angle*np.pi), center[1]), radius + trench_sector + trench_sector/np.sin(angle*np.pi),  initial_angle=initial_angle, final_angle=final_angle, tolerance=0.0001, **LAYER_NEG).rotate(direction*np.pi, center)
    
    path_trench = gdspy.Path(trench_path, (center[0]-1, center[1]))
    path_trench.segment(600 + idx_rings*(2*R+L_coup+100), **LAYER_NEG)
    x_ring = path_trench.x - 100
    y_ring = path_trench.y + gap_coup + WG_WIDTH
    path_trench.turn(R, 'l', **LAYER_NEG)
    path_trench.turn(R, 'r', **LAYER_NEG)
    path_trench.segment(300 + (len(L_coups)-idx_rings-1)*(2*R+L_coup+100), **LAYER_NEG)
    
    ring1_trench = gdspy.Path(trench_path, (x_ring, y_ring))
    ring1_trench.segment(L_coup, **LAYER_NEG)
    ring1_trench.turn(R, 'll', **LAYER_NEG)
    ring1_trench.segment(L_coup, **LAYER_NEG)
    ring1_trench.turn(R, 'll', **LAYER_NEG)

    arc2 = gdspy.copy(arc)
    arc2.rotate(np.pi, (center[0], center[1]))
    arc2.translate(path_trench.x-3200, 2*R)
    
    cell.add(arc).add(path_trench).add(ring1_trench).add(arc2)


# Plot
gdspy.LayoutViewer(lib)

# Write to GDS file
if overwrite:
    lib.write_gds('Shai_SBS_CrMask_V4.gds')

# Enable running on the same kernel
gdspy.current_library = gdspy.GdsLibrary()