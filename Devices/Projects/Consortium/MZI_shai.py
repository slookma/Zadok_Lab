# -*- coding: utf-8 -*-
"""
Created on Wed May 24 22:51:00 2023

@author: benamis9
"""


# Units: um

import numpy
import gdspy
import math


overwrite   = 1 # 1 - Overwrite GDS, 0 - Don't overwrite
add_heater  = 0
lib = gdspy.GdsLibrary()
cell = lib.new_cell('MZI_array')


# Layers:
ld_NWG          = {"layer": 174,    "datatype": 0}
ld_Silox        = {"layer": 9,      "datatype": 0}
ld_taperMark    = {"layer": 118,    "datatype": 120}
ld_GC           = {"layer": 118,    "datatype": 121}
ld_SUS          = {"layer": 195,    "datatype": 0}
ld_VG1          = {"layer": 192,    "datatype": 0}
ld_TNR          = {"layer": 26,     "datatype": 0}
ld_VIA1         = {"layer": 17,     "datatype": 0}
ld_VIA2         = {"layer": 27,     "datatype": 0}
ld_METAL2       = {"layer": 18,     "datatype": 0}
ld_METAL3       = {"layer": 28,     "datatype": 0}
ld_dataExtend   = {"layer": 118,    "datatype": 134}

# Parameters:
width               = 1
taper_len           = 200 - 10
final_taper_width   = 0.3
bend_radius         = 90
safety_gap          = 30
coup_gap            = 0.3
# Lc_vec              = [0,6,8,10,11.85,14,24,26,28] # 50/50 coupler
Lc_vec              = [18,20,29,32,34,36,50,56,59] # 90/10 coupler
chip_size           = 5000 - 20
W_TNRpad            = 21
W_M1pad             = 23
W_via1              = 0.26
W_via2              = 0.5


for idx_col in range(3):
    
    for idx_row in range(3):
        Lc = Lc_vec[idx_row + idx_col*3]
        x_run_start = (15*bend_radius + 2*Lc) * idx_row
        x_run_end   = (15*bend_radius + 2*Lc) * (2 - idx_row)
        ###########################################################################
        # Start path1 (bottom track)
        path1 = gdspy.Path(width, (taper_len, -idx_row*2*safety_gap - idx_col*(4*bend_radius + 3*coup_gap + 5*safety_gap)))
        x_start = path1.x
        y_start = path1.y
        path1.segment(x_run_start, "+x", **ld_NWG)
        path1.segment(2*bend_radius, **ld_NWG)
        # "Bump" for coupler
        path1.turn(bend_radius, "l", **ld_NWG)
        path1.turn(bend_radius, "r", **ld_NWG)
        path1.segment(Lc, **ld_NWG)
        x_coup1_bottom = path1.x
        y_coup1_bottom = path1.y
        path1.turn(bend_radius, "r", **ld_NWG)
        path1.turn(bend_radius, "l", **ld_NWG)
        # "Bump" for extra length
        path1.turn(bend_radius, "l", **ld_NWG)
        path1.turn(bend_radius, "r", **ld_NWG)
        x_middle = path1.x
        y_middle = path1.y
        path1.turn(bend_radius, "r", **ld_NWG)
        path1.turn(bend_radius, "l", **ld_NWG)
        # "Bump" for coupler
        path1.turn(bend_radius, "l", **ld_NWG)
        path1.turn(bend_radius, "r", **ld_NWG)
        path1.segment(Lc, **ld_NWG)
        x_coup2_bottom = path1.x
        y_coup2_bottom = path1.y
        path1.turn(bend_radius, "r", **ld_NWG)
        path1.turn(bend_radius, "l", **ld_NWG)
        # S shape
        path1.turn(bend_radius, "l", **ld_NWG)
        path1.segment(2*bend_radius + coup_gap - safety_gap, **ld_NWG)
        path1.turn(bend_radius, "r", **ld_NWG)
        path1.segment(x_run_end, **ld_NWG)
        x_end = path1.x
        path1.segment(chip_size - x_end - taper_len, **ld_NWG)
        path1.segment(taper_len, final_width=final_taper_width, **ld_NWG)
        path4 = gdspy.Path(width, (x_start, y_start))
        path4.segment(taper_len, "-x", final_width=final_taper_width, **ld_NWG)
        
        ###########################################################################
        # Start path2 + path3 (top track)
        path2 = gdspy.Path(width, (x_coup1_bottom, y_coup1_bottom + width + coup_gap))
        # Right half of the coupler "bump"
        path2.turn(bend_radius, "l", **ld_NWG)
        path2.turn(bend_radius, "r", **ld_NWG)
        if (idx_col == 0) & (idx_row == 0):
            x_heat = path2.x
            y_heat = path2.y
        # Straight section where bottom has "bump"
        path2.segment(4*bend_radius, **ld_NWG)
        # "Bump" for coupler
        path2.turn(bend_radius, "r", **ld_NWG)
        path2.turn(bend_radius, "l", **ld_NWG)
        path2.segment(Lc, **ld_NWG)
        path2.turn(bend_radius, "l", **ld_NWG)
        path2.turn(bend_radius, "r", **ld_NWG)
        # X run while bottom does S shape
        path2.segment(2*bend_radius, **ld_NWG)
        path2.segment(x_run_end, **ld_NWG)
        x_end = path2.x
        path2.segment(chip_size - x_end - taper_len, **ld_NWG)
        path2.segment(taper_len, final_width=final_taper_width, **ld_NWG)
        
        # Back to first coupler, going left
        path3 = gdspy.Path(width, (x_coup1_bottom, y_coup1_bottom + width + coup_gap))
        path3.segment(Lc, "-x", **ld_NWG)
        path3.turn(bend_radius, "r", **ld_NWG)
        path3.turn(bend_radius, "ll", **ld_NWG)
        path3.segment(2*bend_radius + coup_gap - safety_gap, **ld_NWG)
        path3.turn(bend_radius, "r", **ld_NWG)
        path3.segment(x_run_start, **ld_NWG)
        path3.segment(taper_len, final_width=final_taper_width, **ld_NWG)
        
        
        cell.add(path1)
        cell.add(path2)
        cell.add(path3)
        cell.add(path4)


if add_heater == 1:
    path_TNR = gdspy.Path(2*width, (x_heat, y_heat))
    path_TNR.segment(4*bend_radius, **ld_TNR)
    path_TNR.turn(10*width, "l", final_width=6*width, **ld_TNR)
    poly_TNR = gdspy.Polygon([(path_TNR.x - W_TNRpad/2, path_TNR.y),(path_TNR.x + W_TNRpad/2, path_TNR.y),(path_TNR.x + W_TNRpad/2, path_TNR.y + W_TNRpad/2),(path_TNR.x - W_TNRpad/2, path_TNR.y + W_TNRpad/2)], **ld_TNR)
    
    # Add via's from TNR to M1
    for i in range(math.floor(W_TNRpad / W_via1 / 2)):
        for j in range(math.floor(W_TNRpad / W_via1 / 4)):
            x_start_via = path_TNR.x - W_TNRpad/2 + W_via1 + W_via1*2*i
            y_start_via = path_TNR.y + W_via1/2   + W_via1/2 + W_via1*2*j
            polyVia1 = gdspy.Polygon([(x_start_via, y_start_via),(x_start_via + W_via1, y_start_via), (x_start_via + W_via1, y_start_via + W_via1), (x_start_via, y_start_via + W_via1)], **ld_VIA1)
            cell.add(polyVia1)
            
    poly_M1 = gdspy.Polygon([(path_TNR.x - W_M1pad/2, path_TNR.y - (W_M1pad - W_TNRpad)/4),(path_TNR.x + W_M1pad/2, path_TNR.y - (W_M1pad - W_TNRpad)/4),(path_TNR.x + W_M1pad/2, path_TNR.y - (W_M1pad - W_TNRpad)/4 + W_M1pad/2),(path_TNR.x - W_M1pad/2, path_TNR.y - (W_M1pad - W_TNRpad)/4 + W_M1pad/2)], **ld_METAL2)
    
    # Add via's from M1 to M2
    for i in range(math.floor(W_M1pad / W_via2 / 2)):
        for j in range(math.floor(W_M1pad / W_via2 / 4)):
            x_start_via = path_TNR.x - W_M1pad/2 + W_via2/2 + W_via2*2*i
            y_start_via = path_TNR.y - (W_M1pad - W_TNRpad)/4 + W_via2/2   + W_via2/2 + W_via2*2*j
            polyVia2 = gdspy.Polygon([(x_start_via, y_start_via),(x_start_via + W_via2, y_start_via), (x_start_via + W_via2, y_start_via + W_via2), (x_start_via, y_start_via + W_via2)], **ld_VIA2)
            cell.add(polyVia2)
            
    poly_M2 = gdspy.Polygon([(path_TNR.x - W_M1pad/2, path_TNR.y - (W_M1pad - W_TNRpad)/4),(path_TNR.x + W_M1pad/2, path_TNR.y - (W_M1pad - W_TNRpad)/4),(path_TNR.x + W_M1pad/2, path_TNR.y - (W_M1pad - W_TNRpad)/4 + W_M1pad/2),(path_TNR.x - W_M1pad/2, path_TNR.y - (W_M1pad - W_TNRpad)/4 + W_M1pad/2)], **ld_METAL3)
    path_M2 = gdspy.Path(W_M1pad, (path_TNR.x, path_TNR.y - (W_M1pad - W_TNRpad)/4 + W_M1pad/2))
    path_M2.segment(W_M1pad*3, "+y", **ld_METAL3)
    poly2_M2 = gdspy.Polygon([(path_M2.x - W_M1pad/2, path_M2.y - (W_M1pad - W_TNRpad)/4),(path_TNR.x + W_M1pad/2, path_TNR.y - (W_M1pad - W_TNRpad)/4),(path_TNR.x + W_M1pad/2, path_TNR.y - (W_M1pad - W_TNRpad)/4 + W_M1pad/2),(path_TNR.x - W_M1pad/2, path_TNR.y - (W_M1pad - W_TNRpad)/4 + W_M1pad/2)], **ld_METAL3)
    

    cell.add(path_TNR)
    cell.add(poly_TNR)
    cell.add(poly_M1)
    cell.add(poly_M2)
    cell.add(path_M2)

gdspy.LayoutViewer(lib)
if overwrite == 1:
    lib.write_gds("MZI.gds")