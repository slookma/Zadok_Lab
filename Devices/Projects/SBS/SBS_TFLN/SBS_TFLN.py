# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 11:42:30 2026

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

overwrite = 0 # 1 - Overwrite GDS, 0 - Don't overwrite
lib = gdspy.GdsLibrary()


# cells = [gdspy.Cell(f"SBS_TFLN{i}") for i in range(10)]
cells = [lib.new_cell(f"SBS_TFLN{i}") for i in range(10)]

# cells = [lib.new_cell('SBS_TFLN1'), lib.new_cell('SBS_TFLN2')]

# Layers:
ld_SiN = {"layer": 1,    "datatype": 0}

# Parameters:
WG_WIDTH        = 2.1
EL_WIDTH        = 4
bend_radius     = 300
EL_bend_radius  = EL_WIDTH/2
Hbend           = 200
Lbend           = 400
safety_gap      = 100
coup_gap        = 1.2
opt_arr_gap     = 127
el_arr_gap      = 125
Hbend           = 200
Lbend           = 800
chip_sizeX      = 10000
chip_sizeY      = 10000

# Wifi parameters:
period    = 1
fill_frac = 0.5
layer1    = 50
layer2    = 49
layer3    = 48
datatype  = 0
FF        = 0.8
teeth     = 90
radius    = 150
angle     = 0.1
LAYER_WG  = {"layer": layer1, "datatype": datatype}
LAYER_NEG = {"layer": layer2, "datatype": datatype}
LAYER_MET = {"layer": layer3, "datatype": datatype}

# IDT parameters:
lambda0   = 1.55
neff      = 1.6182 # ZEP e cut: 1.6182 ; ZEP o cut: 1.65 ; maN e cut: 1.6508 ; maN o cut: 1.6821
IDT_per   = lambda0/(2*neff)
IDT_DC    = 0.5
IDT_width = IDT_per*IDT_DC/2
IDT_teeth = 600

## U shape
center = (500,0)
path1 = create_grating_path(cells[0], period, fill_frac, teeth, center, radius, angle, WG_WIDTH, direction=1,
                                    LAYER_WG={"layer": layer1, "datatype": datatype})
path1.segment(700, "+y",  **LAYER_WG)
path1.turn(bend_radius, 'r', **LAYER_WG)
path1.segment(15*opt_arr_gap-2*bend_radius, "+x", **LAYER_WG)
path1.turn(bend_radius, 'r', **LAYER_WG)
path1.segment(700, "-y",  **LAYER_WG)
x_curr = path1.x
y_curr = path1.y
path2 = create_grating_path(cells[1], period, fill_frac, teeth, (x_curr, center[1]), radius, angle, WG_WIDTH, direction=1,
                                    LAYER_WG={"layer": layer1, "datatype": datatype})


## Ring
center = (5500,0)
path3 = create_grating_path(cells[2], period, fill_frac, teeth, center, radius, angle, WG_WIDTH, direction=1,
                                    LAYER_WG={"layer": layer1, "datatype": datatype})
path3.segment(700, "+y",  **LAYER_WG)
path3.turn(bend_radius, 'r', **LAYER_WG)
path3.segment(15*opt_arr_gap-2*bend_radius, "+x", **LAYER_WG)
path3.turn(bend_radius, 'r', **LAYER_WG)
path3.segment(700, "-y",  **LAYER_WG)
x_curr = path3.x
y_curr = path3.y
path4 = create_grating_path(cells[3], period, fill_frac, teeth, (x_curr, center[1]), radius, angle, WG_WIDTH, direction=1,
                                    LAYER_WG={"layer": layer1, "datatype": datatype})

path5 = gdspy.Path(WG_WIDTH, (x_curr-(15*opt_arr_gap)/2, y_curr+700+bend_radius+WG_WIDTH+coup_gap))
path5.turn(bend_radius, 'l', **LAYER_WG)
path5.segment(200, "+y",  **LAYER_WG)
path5.turn(bend_radius, 'll', **LAYER_WG)
path5.segment(200, "-y",  **LAYER_WG)
path5.turn(bend_radius, 'l', **LAYER_WG)
cells[2].add(path5)



## long
center = (0,-6000)
path6 = create_grating_path(cells[4], period, fill_frac, teeth, center, radius, angle, WG_WIDTH, direction=0,
                                    LAYER_WG={"layer": layer1, "datatype": datatype})
path6.segment(500, "+x",  **LAYER_WG)
path6.turn(bend_radius, 'l', **LAYER_WG)
path6.segment(400, "+y",  **LAYER_WG)
path6.turn(bend_radius, 'r', **LAYER_WG)
path6.segment(7000, "+x",  **LAYER_WG)
path6.turn(bend_radius, 'r', **LAYER_WG)
path6.segment(600, "-y",  **LAYER_WG)
path6.turn(bend_radius, 'l', **LAYER_WG)
path6.segment(500, "+x",  **LAYER_WG)
x_curr = path6.x
y_curr = path6.y
path7 = create_grating_path(cells[5], period, fill_frac, teeth, (x_curr-3.25, y_curr), radius, angle, WG_WIDTH, direction=2,
                                    LAYER_WG={"layer": layer1, "datatype": datatype})

# Pads
corner = (1337.5,-600)
side = 100
for idx in range(16):
    points = [(corner[0]+idx*el_arr_gap,      corner[1]),
              (corner[0]+idx*el_arr_gap+side, corner[1]), 
              (corner[0]+idx*el_arr_gap+side, corner[1]+side), 
              (corner[0]+idx*el_arr_gap,      corner[1]+side)]
    pad = gdspy.Polygon(points, **LAYER_MET)
    cells[6].add(pad)


# IDT 1:
path_EL1 = gdspy.Path(EL_WIDTH, (corner[0]+side/2,corner[1]+side))
path_EL1.segment(100, "+y", **LAYER_MET)
path_EL1.turn(EL_bend_radius, 'l', **LAYER_MET)
path_EL1.segment(abs(-400-path_EL1.x), "-x", **LAYER_MET)
path_EL1.turn(EL_bend_radius, 'r', **LAYER_MET)
path_EL1.segment(abs(500-path_EL1.y), "+y", **LAYER_MET)
path_EL1.turn(EL_bend_radius, 'r', **LAYER_MET)
path_EL1.segment(abs(400-path_EL1.x), "+x", **LAYER_MET)
x_IDT_bot = path_EL1.x
y_IDT_bot = path_EL1.y
cells[6].add(path_EL1)

path_EL2 = gdspy.Path(EL_WIDTH, (corner[0]+el_arr_gap+side/2,corner[1]))
path_EL2.segment(100, "-y", **LAYER_MET)
path_EL2.turn(EL_bend_radius, 'r', **LAYER_MET)
path_EL2.segment(2275, "-x", **LAYER_MET)
path_EL2.turn(EL_bend_radius, 'r', **LAYER_MET)
path_EL2.segment(2800, "+y", **LAYER_MET)
path_EL2.turn(EL_bend_radius, 'r', **LAYER_MET)
path_EL2.segment(800, "+x", **LAYER_MET)
x_IDT_top = path_EL2.x
y_IDT_top = path_EL2.y
cells[6].add(path_EL2)

for idx in range(IDT_teeth):
    path_IDT = gdspy.Path(IDT_width, (x_IDT_bot-IDT_width/2-idx*IDT_per,y_IDT_bot))
    path_IDT.segment(950, "+y", **LAYER_MET)
    cells[6].add(path_IDT)
    path_IDT = gdspy.Path(IDT_width, (x_IDT_top-IDT_per/2-IDT_width/2-idx*IDT_per,y_IDT_top))
    path_IDT.segment(950, "-y", **LAYER_MET)
    cells[6].add(path_IDT)


# IDT 2:
path_EL3 = gdspy.Path(EL_WIDTH, (corner[0]+2*el_arr_gap+side/2,corner[1]+side))
path_EL3.segment(750, "+y", **LAYER_MET)
path_EL3.turn(EL_bend_radius, 'rr', **LAYER_MET)
path_EL3.turn(EL_bend_radius, 'll', **LAYER_MET)
path_EL3.turn(EL_bend_radius, 'rr', **LAYER_MET)
path_EL3.turn(EL_bend_radius, 'll', **LAYER_MET)
path_EL3.segment(850, "+y", **LAYER_MET)
path_EL3.turn(EL_bend_radius, 'l', **LAYER_MET)
path_EL3.segment(1895, "-x", **LAYER_MET)
x_IDT_bot = path_EL3.x
y_IDT_bot = path_EL3.y
cells[6].add(path_EL3)

path_EL4 = gdspy.Path(EL_WIDTH, (corner[0]+3*el_arr_gap+side/2,corner[1]+side))
path_EL4.segment(0, "+y", **LAYER_MET)
path_EL4.turn(EL_bend_radius, 'r', **LAYER_MET)
path_EL4.segment(2051.22, "+x", **LAYER_MET)
path_EL4.turn(EL_bend_radius, 'l', **LAYER_MET)
path_EL4.segment(2000, "+y", **LAYER_MET)
path_EL4.turn(EL_bend_radius, 'l', **LAYER_MET)
path_EL4.segment(2271.22, "-x", **LAYER_MET)
x_IDT_top = path_EL4.x
y_IDT_top = path_EL4.y
cells[6].add(path_EL4)

for idx in range(IDT_teeth):
    path_IDT = gdspy.Path(IDT_width, (x_IDT_bot+IDT_width/2+idx*IDT_per,y_IDT_bot))
    path_IDT.segment(950, "+y", **LAYER_MET)
    cells[6].add(path_IDT)
    path_IDT = gdspy.Path(IDT_width, (x_IDT_top+IDT_per/2+IDT_width/2+idx*IDT_per,y_IDT_top))
    path_IDT.segment(950, "-y", **LAYER_MET)
    cells[6].add(path_IDT)


# IDT 3:
path_EL5 = gdspy.Path(EL_WIDTH, (corner[0]+4*el_arr_gap+side/2,corner[1]))
path_EL5.segment(200, "-y", **LAYER_MET)
path_EL5.turn(EL_bend_radius, 'r', **LAYER_MET)
path_EL5.segment(2250, "-x", **LAYER_MET)
path_EL5.turn(EL_bend_radius, 'l', **LAYER_MET)
path_EL5.segment(2900, "-y", **LAYER_MET)
path_EL5.turn(EL_bend_radius, 'l', **LAYER_MET)
path_EL5.segment(700, "+x", **LAYER_MET)
x_IDT_bot = path_EL5.x
y_IDT_bot = path_EL5.y
cells[6].add(path_EL5)

path_EL6 = gdspy.Path(EL_WIDTH, (corner[0]+5*el_arr_gap+side/2,corner[1]))
path_EL6.segment(1000, "-y", **LAYER_MET)
path_EL6.turn(EL_bend_radius, 'rr', **LAYER_MET)
path_EL6.segment(140.26, "+y", **LAYER_MET)
path_EL6.turn(EL_bend_radius, 'l', **LAYER_MET)
path_EL6.segment(1600, "-x", **LAYER_MET)
path_EL6.turn(EL_bend_radius, 'l', **LAYER_MET)
path_EL6.segment(1840.26, "-y", **LAYER_MET)
path_EL6.turn(EL_bend_radius, 'l', **LAYER_MET)
path_EL6.segment(225, "+x", **LAYER_MET)
path_EL6.turn(EL_WIDTH/2, 'l', **LAYER_MET)
path_EL6.segment(20, "+y", **LAYER_MET)
path_EL6.turn(EL_WIDTH/2, 'r', **LAYER_MET)
path_EL6.segment(300, "+x", **LAYER_MET)
x_IDT_top = path_EL6.x
y_IDT_top = path_EL6.y
cells[6].add(path_EL6)

for idx in range(IDT_teeth):
    path_IDT = gdspy.Path(IDT_width, (x_IDT_bot-IDT_width/2-idx*IDT_per,y_IDT_bot))
    path_IDT.segment(950, "+y", **LAYER_MET)
    cells[6].add(path_IDT)
    path_IDT = gdspy.Path(IDT_width, (x_IDT_top-IDT_per/2-IDT_width/2-idx*IDT_per,y_IDT_top))
    path_IDT.segment(950, "-y", **LAYER_MET)
    cells[6].add(path_IDT)


###################################
## Add text
###################################

###################################
## Add markers
###################################



gdspy.LayoutViewer(lib)
if overwrite == 1:
    lib.write_gds("SBS_TFLN.gds")
    
# Enable running on the same kernel
gdspy.current_library = gdspy.GdsLibrary
