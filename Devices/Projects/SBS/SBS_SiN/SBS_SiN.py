# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 15:46:10 2026

@author: USER
"""

# Units: um

import gdspy
import math
from s_bend_func import sbendPath, sbendPathM

overwrite   = 0 # 1 - Overwrite GDS, 0 - Don't overwrite
lib = gdspy.GdsLibrary()
cell = lib.new_cell('SBS_SiN')


# Layers:
ld_SiN          = {"layer": 1,    "datatype": 0}

# Parameters:
width               = 1
taper_len           = 500
final_taper_width   = 0.3
bend_radius         = 100
Hbend               = 200
Lbend               = 400
safety_gap          = 100
coup_gap            = 0.2
Lc_vec              = [21, 23, 25, 27, 29, 31]
Nturns              = 5
chip_sizeX          = 5000
chip_sizeY          = 5000

###################################
## Add stripes for polishing + text
###################################

###################################
## Add markers
###################################

## Short WG
path1 = gdspy.Path(width, (-chip_sizeX/2 + taper_len, chip_sizeY/2 - 500))
x_start = path1.x
y_start = path1.y
sbendPathM(path1,Lbend, Hbend, ld_SiN)
path1.segment(chip_sizeX - Lbend - 2*taper_len, "+x", **ld_SiN)
x_end = path1.x
y_end = path1.y
path1.segment(taper_len, final_width=final_taper_width, **ld_SiN)
path2 = gdspy.Path(width, (x_start, y_start))
path2.segment(taper_len, "-x", final_width=final_taper_width, **ld_SiN)

cell.add(path1)
cell.add(path2)

## Long WG
path3 = gdspy.Path(width, (-chip_sizeX/2 + taper_len, y_end - safety_gap))
x_start = path3.x
y_start = path3.y
path3.segment(bend_radius, "+x", **ld_SiN)
for idx in range(Nturns):
    path3.segment(chip_sizeX - 2*taper_len - 2*bend_radius, "+x", **ld_SiN)
    path3.turn(bend_radius, 'rr', **ld_SiN)
    path3.segment(chip_sizeX - 2*taper_len - 2*bend_radius, "-x", **ld_SiN)
    path3.turn(bend_radius, 'll', **ld_SiN)

path3.segment(chip_sizeX - 2*taper_len - bend_radius, "+x", **ld_SiN)
x_end = path3.x
y_end = path3.y
path3.segment(taper_len, final_width=final_taper_width, **ld_SiN)
path4 = gdspy.Path(width, (x_start, y_start))
path4.segment(taper_len, "-x", final_width=final_taper_width, **ld_SiN)

cell.add(path3)
cell.add(path4)


## Rings
for idx in range(len(Lc_vec)):
    Lc = Lc_vec[idx]
    path5 = gdspy.Path(width, (-chip_sizeX/2 + taper_len, y_end - safety_gap))
    x_start = path5.x
    y_start = path5.y
    sbendPathM(path5,Lbend, Hbend, ld_SiN)
    path5.segment(chip_sizeX - Lbend - 2*taper_len, "+x", **ld_SiN)
    x_end = path5.x
    y_end = path5.y
    path5.segment(taper_len, final_width=final_taper_width, **ld_SiN)
    path6 = gdspy.Path(width, (x_start, y_start))
    path6.segment(taper_len, "-x", final_width=final_taper_width, **ld_SiN)
    path7 = gdspy.Path(width, (0, y_end + coup_gap + width))
    path7.segment(Lc, "+x", **ld_SiN)
    path7.turn(bend_radius, 'll', **ld_SiN)
    path7.segment(Lc, "-x", **ld_SiN)
    path7.turn(bend_radius, 'll', **ld_SiN)
    
    # Text
    htext1 = gdspy.Text("Lc = " + str(Lc) + "um", 20, (-chip_sizeX/2 + taper_len/2, y_start + 10), **ld_SiN)
    htext2 = gdspy.Text("Lc = " + str(Lc) + "um", 20, (chip_sizeX/2  - taper_len/2, y_end   + 10), **ld_SiN)
    
    cell.add(path5)
    cell.add(path6)
    cell.add(path7)
    cell.add(htext1)
    cell.add(htext2)
    
    
## Stripes for polishing
for idx in range(10):
    path8 = gdspy.Path(2.5, (-chip_sizeX/2 + idx*10, chip_sizeY/2 - 650))
    path8.segment(10, "+y", **ld_SiN)
    cell.add(path8)
    
for idx in range(10):
    path9 = gdspy.Path(2.5, (-chip_sizeX/2 + idx*10, -chip_sizeY/2 + 650))
    path9.segment(10, "+y", **ld_SiN)
    cell.add(path9)
    
for idx in range(10):
    path10 = gdspy.Path(2.5, (chip_sizeX/2 - idx*10, chip_sizeY/2 - 650))
    path10.segment(10, "+y", **ld_SiN)
    cell.add(path10)
    
for idx in range(10):
    path11 = gdspy.Path(2.5, (chip_sizeX/2 - idx*10, -chip_sizeY/2 + 650))
    path11.segment(10, "+y", **ld_SiN)
    cell.add(path11)


gdspy.LayoutViewer(lib)
if overwrite == 1:
    lib.write_gds("SBS_SiN.gds")
    
gdspy.current_library = gdspy.GdsLibrary()