# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 01:15:12 2026

@author: USER
"""
# Units: um

import gdspy
import math
import sys
import numpy as np
sys.path.insert(0, "C:/Users/USER/GitHub/Zadok_Lab/Devices/Projects/Consortium")
from s_bend_func import sbendPath, sbendPathM
from maayan_wifi import create_grating_path

overwrite = 1 # 1 - Overwrite GDS, 0 - Don't overwrite
lib = gdspy.GdsLibrary()
cell = lib.new_cell('IDT_sweep')

# Parameters:
EL_WIDTH        = 4
EL_bend_radius  = 20
safety_gap      = 100
el_arr_gap      = 125
side            = 100
chip_sizeX      = 10000
chip_sizeY      = 10000
IDT_sep_vec     = [1000, 500, 100, 50, 10]
IDT_per_vec     = [10, 5, 1, 0.5]
layer1          = 1
layer2          = 2
datatype        = 0
text_size       = 40


LAYER_MET = {"layer": layer1, "datatype": datatype}
LAYER_IDT = {"layer": layer2, "datatype": datatype}


for idx_per in range(len(IDT_per_vec)):
    for idx_sep in range(len(IDT_sep_vec)):
        # IDT parameters:
        lambda0     = 1.55
        neff        = 1.6182 # ZEP e cut: 1.6182 ; ZEP o cut: 1.65 ; maN e cut: 1.6508 ; maN o cut: 1.6821
        # IDT_per     = lambda0/(2*neff)
        IDT_per     = IDT_per_vec[idx_per]
        IDT_DC      = 0.5
        IDT_width   = IDT_per*IDT_DC/2
        IDT_teeth   = 20
        IDT_height  = 250
        IDT_gap     = 10
        IDT_sep     = IDT_sep_vec[idx_sep]
        I           = IDT_teeth*IDT_per
        x1          = 500
        x2          = x1+I+IDT_sep/2
        y1          = 100
        y2          = 200
        Dy          = (5/2-9/8*np.pi)*EL_bend_radius+0.25*(side+IDT_height+IDT_gap+el_arr_gap)
        
        # Pads
        corner = (idx_sep*2800,-idx_per*800)
        for idx in range(4):
            points = [(corner[0]+idx*el_arr_gap,      corner[1]),
                      (corner[0]+idx*el_arr_gap+side, corner[1]), 
                      (corner[0]+idx*el_arr_gap+side, corner[1]+side), 
                      (corner[0]+idx*el_arr_gap,      corner[1]+side)]
            pad = gdspy.Polygon(points, **LAYER_MET)
            cell.add(pad)
        
        
        # IDT 1:
        path_EL1 = gdspy.Path(EL_WIDTH, (corner[0],corner[1]+side/2))
        path_EL1.segment(x2+EL_bend_radius, "-x", **LAYER_MET)
        path_EL1.turn(EL_bend_radius, 'l', **LAYER_MET)
        path_EL1.segment(side/2+y1+y2+IDT_height+IDT_gap+EL_bend_radius, "-y", **LAYER_MET)
        path_EL1.turn(EL_bend_radius, 'l', **LAYER_MET)
        path_EL1.segment(1.5*el_arr_gap+side/2+x2-IDT_sep/2+EL_bend_radius, "+x", **LAYER_MET)
        x_IDT_bot = path_EL1.x
        y_IDT_bot = path_EL1.y
        cell.add(path_EL1)
        
        path_EL2 = gdspy.Path(EL_WIDTH, (corner[0]+el_arr_gap+side/2,corner[1]))
        path_EL2.segment(y1, "-y", **LAYER_MET)
        path_EL2.turn(EL_bend_radius, 'r', **LAYER_MET)
        path_EL2.segment(x2, "-x", **LAYER_MET)
        path_EL2.turn(EL_bend_radius, 'l', **LAYER_MET)
        path_EL2.segment(y2, "-y", **LAYER_MET)
        path_EL2.turn(EL_bend_radius, 'l', **LAYER_MET)
        path_EL2.segment(el_arr_gap/2+x2-IDT_sep/2-500, "+x", **LAYER_MET)
        path_EL2.turn(EL_bend_radius, 'r', **LAYER_MET)
        path_EL2.segment(Dy, "-y", **LAYER_MET)
        path_EL2.turn(EL_bend_radius, 'll', **LAYER_MET)
        path_EL2.segment(Dy, "+y", **LAYER_MET)
        path_EL2.turn(EL_bend_radius, 'rr', **LAYER_MET)
        path_EL2.segment(Dy, "-y", **LAYER_MET)
        path_EL2.turn(EL_bend_radius, 'll', **LAYER_MET)
        path_EL2.segment(Dy, "+y", **LAYER_MET)
        path_EL2.turn(EL_bend_radius, 'r', **LAYER_MET)
        path_EL2.segment(500-7*EL_bend_radius, "+x", **LAYER_MET)
        x_IDT_top = path_EL2.x
        y_IDT_top = path_EL2.y
        cell.add(path_EL2)
        
        for idx in range(IDT_teeth):
            path_IDT = gdspy.Path(IDT_width, (x_IDT_bot-IDT_width/2-idx*IDT_per,y_IDT_bot))
            path_IDT.segment(IDT_height, "+y", **LAYER_IDT)
            cell.add(path_IDT)
            path_IDT = gdspy.Path(IDT_width, (x_IDT_top-IDT_per/2-IDT_width/2-idx*IDT_per,y_IDT_top))
            path_IDT.segment(IDT_height, "-y", **LAYER_IDT)
            cell.add(path_IDT)
        
        
        # IDT 2:
        path_EL3 = gdspy.Path(EL_WIDTH, (corner[0]+3*el_arr_gap+side,corner[1]+side/2))
        path_EL3.segment(x2+EL_bend_radius, "+x", **LAYER_MET)
        path_EL3.turn(EL_bend_radius, 'r', **LAYER_MET)
        path_EL3.segment(side/2+y1+y2+IDT_height+IDT_gap+EL_bend_radius, "-y", **LAYER_MET)
        path_EL3.turn(EL_bend_radius, 'r', **LAYER_MET)
        path_EL3.segment(1.5*el_arr_gap+side/2+x2-IDT_sep/2+EL_bend_radius, "-x", **LAYER_MET)
        x_IDT_bot = path_EL3.x
        y_IDT_bot = path_EL3.y
        cell.add(path_EL3)
        
        path_EL4 = gdspy.Path(EL_WIDTH, (corner[0]+2*el_arr_gap+side/2,corner[1]))
        path_EL4.segment(y1, "-y", **LAYER_MET)
        path_EL4.turn(EL_bend_radius, 'l', **LAYER_MET)
        path_EL4.segment(x2, "+x", **LAYER_MET)
        path_EL4.turn(EL_bend_radius, 'r', **LAYER_MET)
        path_EL4.segment(y2, "-y", **LAYER_MET)
        path_EL4.turn(EL_bend_radius, 'r', **LAYER_MET)
        path_EL4.segment(el_arr_gap/2+x2-IDT_sep/2-500, "-x", **LAYER_MET)
        path_EL4.turn(EL_bend_radius, 'l', **LAYER_MET)
        path_EL4.segment(Dy, "-y", **LAYER_MET)
        path_EL4.turn(EL_bend_radius, 'rr', **LAYER_MET)
        path_EL4.segment(Dy, "+y", **LAYER_MET)
        path_EL4.turn(EL_bend_radius, 'll', **LAYER_MET)
        path_EL4.segment(Dy, "-y", **LAYER_MET)
        path_EL4.turn(EL_bend_radius, 'rr', **LAYER_MET)
        path_EL4.segment(Dy, "+y", **LAYER_MET)
        path_EL4.turn(EL_bend_radius, 'l', **LAYER_MET)
        path_EL4.segment(500-7*EL_bend_radius, "-x", **LAYER_MET)
        x_IDT_top = path_EL4.x
        y_IDT_top = path_EL4.y
        cell.add(path_EL4)
        
        for idx in range(IDT_teeth):
            path_IDT = gdspy.Path(IDT_width, (x_IDT_bot+IDT_width/2+idx*IDT_per,y_IDT_bot))
            path_IDT.segment(IDT_height, "+y", **LAYER_IDT)
            cell.add(path_IDT)
            path_IDT = gdspy.Path(IDT_width, (x_IDT_top+IDT_per/2+IDT_width/2+idx*IDT_per,y_IDT_top))
            path_IDT.segment(IDT_height, "-y", **LAYER_IDT)
            cell.add(path_IDT)
            
        # Text:
        IDT_text = gdspy.Text("Period = " + str(IDT_per) + "um ; Gap = " + str(IDT_sep) + "um", text_size, (corner[0]-260,corner[1]-y1-text_size-100), **LAYER_IDT)
        cell.add(IDT_text)


###################################
## Add text
###################################

###################################
## Add markers
###################################



gdspy.LayoutViewer(lib)
if overwrite == 1:
    lib.write_gds("IDT_sweep.gds")
    
# Enable running on the same kernel
gdspy.current_library = gdspy.GdsLibrary
