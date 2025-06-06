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
WG_length       = 6000
copies          = 5
vertical_gap    = 200
L_coups         = list([5,6,7,8])
R               = 200
gap_coup        = 0.2

# Create GDS library and cell
lib        = gdspy.GdsLibrary()
cell       = lib.new_cell('Shai_WIFI')
cell_neg   = lib.new_cell('Shai_WIFI_negative')
cell_final = lib.new_cell('Shai_WIFI_final')

# Parameters
teeth = 90
radius = 90
angle = 0.1
direction = 0
LAYER_WG  = {"layer": layer1, "datatype": datatype}
LAYER_NEG = {"layer": layer2, "datatype": datatype}

for idx_DC, fill_frac in enumerate(fill_fracs):
    for idx_per, period in enumerate(periods):
        center = (0, -(idx_per + idx_DC*len(periods))*vertical_gap)
        # Call the function to create the grating path
        path1 = create_grating_path(cell, period, fill_frac, teeth, center, radius, angle, WG_WIDTH, direction, LAYER_WG=LAYER_WG)
        path1.segment(WG_length/2 - 500, **LAYER_WG)
        sbendPath(path1, 1000, 100, LAYER_WG)
        path1.segment(WG_length/2 - 500, **LAYER_WG)
        cell.add(path1)
        create_grating_path(cell, period, fill_frac, teeth, (path1.x + WG_WIDTH / (2*np.tan((1 - angle) * np.pi)), path1.y), radius, angle,WG_WIDTH, 1, LAYER_WG=LAYER_WG)
        
        # temp1 = gdspy.boolean(cell, cell, "and")
        
        if negative:
            initial_angle = (1 - angle) * np.pi
            final_angle   = (1 + angle) * np.pi
            arc = gdspy.Round((center[0]+trench/np.sin(angle*np.pi), center[1]), radius + trench + trench/np.sin(angle*np.pi),  initial_angle=initial_angle, final_angle=final_angle, tolerance=0.0001, **LAYER_NEG).rotate(direction*np.pi, center)
            
            path_trench = gdspy.Path(WG_WIDTH + trench*2, (center[0]-1, center[1]))
            path_trench.segment(WG_length/2 - 500, '+x', **LAYER_NEG)
            sbendPath(path_trench, 1000, 100, LAYER_NEG)
            path_trench.segment(WG_length/2 - 500 + 6.5, '+x', **LAYER_NEG)
            
            arc2 = gdspy.copy(arc)
            arc2.translate(WG_length, 100)
            arc2.rotate(np.pi, (path1.x, path1.y))
            
            cell_neg.add(arc).add(path_trench).add(arc2)
            
            # temp2 = gdspy.boolean(cell_neg, cell_neg, "and")
            
            # negative_mask = gdspy.boolean(temp2, temp1, "not")
            
            # cell_final.add(negative_mask)

# Add Rings
period    = 0.550
fill_frac = 0.5
for idx_rings, L_coup in enumerate(L_coups):
    center = (0, -(len(periods)*len(fill_fracs)+1)*vertical_gap - idx_rings*vertical_gap - R)
    # Call the function to create the grating path
    path1 = create_grating_path(cell, period, fill_frac, teeth, center, radius, angle, WG_WIDTH, direction, LAYER_WG=LAYER_WG)
    path1.segment(600 + idx_rings*(2*R+L_coup+100), **LAYER_WG)
    x_ring = path1.x - 100
    y_ring = path1.y + gap_coup + WG_WIDTH
    path1.turn(R, 'l', **LAYER_WG)
    path1.turn(R, 'r', **LAYER_WG)
    path1.segment(300 + (len(L_coups)-idx_rings-1)*(2*R+L_coup+100), **LAYER_WG)
    cell.add(path1)
    create_grating_path(cell, period, fill_frac, teeth, (path1.x + WG_WIDTH / (2*np.tan((1 - angle) * np.pi)), path1.y), radius, angle,WG_WIDTH, 1, LAYER_WG=LAYER_WG)
    ring1 = gdspy.Path(WG_WIDTH, (x_ring, y_ring))
    ring1.segment(L_coup, **LAYER_WG)
    ring1.turn(R, 'll', **LAYER_WG)
    ring1.segment(L_coup, **LAYER_WG)
    ring1.turn(R, 'll', **LAYER_WG)
    cell.add(ring1)
    
    if negative:
        initial_angle = (1 - angle) * np.pi
        final_angle   = (1 + angle) * np.pi
        arc = gdspy.Round((center[0]+trench/np.sin(angle*np.pi), center[1]), radius + trench + trench/np.sin(angle*np.pi),  initial_angle=initial_angle, final_angle=final_angle, tolerance=0.0001, **LAYER_NEG).rotate(direction*np.pi, center)
        
        path_trench = gdspy.Path(WG_WIDTH + trench*2, (center[0]-1, center[1]))
        path_trench.segment(600 + idx_rings*(2*R+L_coup+100), **LAYER_NEG)
        path_trench.turn(R, 'l', **LAYER_NEG)
        path_trench.turn(R, 'r', **LAYER_NEG)
        path_trench.segment(300 + (len(L_coups)-idx_rings-1)*(2*R+L_coup+100), **LAYER_NEG)
        
        arc2 = gdspy.copy(arc)
        arc2.rotate(np.pi, (center[0], center[1]))
        arc2.translate(path_trench.x - 1, 2*R)
        
        ring1_neg = gdspy.Path(WG_WIDTH + trench*2, (x_ring, y_ring))
        ring1_neg.segment(L_coup, **LAYER_NEG)
        ring1_neg.turn(R, 'll', **LAYER_NEG)
        ring1_neg.segment(L_coup, **LAYER_NEG)
        ring1_neg.turn(R, 'll', **LAYER_NEG)
        
        cell_neg.add(arc).add(path_trench).add(arc2).add(ring1_neg)
    
# Add Rings
for idx_rings, L_coup in enumerate(L_coups):
    center = (3200, -(len(periods)*len(fill_fracs)+1)*vertical_gap - idx_rings*vertical_gap - R)
    # Call the function to create the grating path
    path1 = create_grating_path(cell, period, fill_frac, teeth, center, radius, angle, WG_WIDTH, direction, LAYER_WG=LAYER_WG)
    path1.segment(600 + idx_rings*(2*R+L_coup+100), **LAYER_WG)
    x_ring = path1.x - 100
    y_ring = path1.y + gap_coup + WG_WIDTH
    path1.turn(R, 'l', **LAYER_WG)
    path1.turn(R, 'r', **LAYER_WG)
    path1.segment(300 + (len(L_coups)-idx_rings-1)*(2*R+L_coup+100), **LAYER_WG)
    cell.add(path1)
    create_grating_path(cell, period, fill_frac, teeth, (path1.x + WG_WIDTH / (2*np.tan((1 - angle) * np.pi)), path1.y), radius, angle,WG_WIDTH, 1, LAYER_WG=LAYER_WG)
    ring1 = gdspy.Path(WG_WIDTH, (x_ring, y_ring))
    ring1.segment(L_coup, **LAYER_WG)
    ring1.turn(R, 'll', **LAYER_WG)
    ring1.segment(L_coup, **LAYER_WG)
    ring1.turn(R, 'll', **LAYER_WG)
    cell.add(ring1)
    
    if negative:
        initial_angle = (1 - angle) * np.pi
        final_angle   = (1 + angle) * np.pi
        arc = gdspy.Round((center[0]+trench/np.sin(angle*np.pi), center[1]), radius + trench + trench/np.sin(angle*np.pi),  initial_angle=initial_angle, final_angle=final_angle, tolerance=0.0001, **LAYER_NEG).rotate(direction*np.pi, center)
        
        path_trench = gdspy.Path(WG_WIDTH + trench*2, (center[0]-1, center[1]))
        path_trench.segment(600 + idx_rings*(2*R+L_coup+100), **LAYER_NEG)
        path_trench.turn(R, 'l', **LAYER_NEG)
        path_trench.turn(R, 'r', **LAYER_NEG)
        path_trench.segment(300 + (len(L_coups)-idx_rings-1)*(2*R+L_coup+100), **LAYER_NEG)
        
        arc2 = gdspy.copy(arc)
        arc2.rotate(np.pi, (center[0], center[1]))
        arc2.translate(path_trench.x - 3200 - 1, 2*R)
        
        ring1_neg = gdspy.Path(WG_WIDTH + trench*2, (x_ring, y_ring))
        ring1_neg.segment(L_coup, **LAYER_NEG)
        ring1_neg.turn(R, 'll', **LAYER_NEG)
        ring1_neg.segment(L_coup, **LAYER_NEG)
        ring1_neg.turn(R, 'll', **LAYER_NEG)
        
        cell_neg.add(arc).add(path_trench).add(arc2).add(ring1_neg)



# Plot
gdspy.LayoutViewer(lib)

# Write to GDS file
if overwrite:
    lib.write_gds('Shai_SBS_V4.gds')

# Enable running on the same kernel
gdspy.current_library = gdspy.GdsLibrary()