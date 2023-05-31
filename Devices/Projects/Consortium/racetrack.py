# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 11:54:46 2022

@author: dokhanl
"""

import gdspy
import numpy as np
import math

# # The GDSII file is called a library, which contains multiple cells.
# lib = gdspy.GdsLibrary()

# # Geometry must be placed in cells.
# cell = lib.new_cell('FIRST')

# # Create the geometry (a single rectangle) and add it to the cell.
# rect = gdspy.Rectangle((0, 0), (2, 1))
# cell.add(rect)

# # Save the library in a file called 'first.gds'.
# lib.write_gds('first.gds')

# # Optionally, save an image of the cell as SVG.
# cell.write_svg('first.svg')

# # Display all cells using the internal viewer.
# gdspy.LayoutViewer()


overwrite = 0 # 1 - Overwrite GDS, 0 - Don't overwrite

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
ld_METAL1       = {"layer": 18,     "datatype": 0}
ld_METAL2       = {"layer": 28,     "datatype": 0}
ld_dataExtend   = {"layer": 118,    "datatype": 134}

# Parameters:
width               = 1
chip_size           = 5000
taper_len           = 200
final_taper_width   = 0.3
bend_radius         = 80
ring_radius         = 100
race_track_len      = 60
N_rings_met         = 5 # How many rings should include metallic grating
N_stripes           = 30
size_stripes        = 60
stripes_gap         = 5
Lc                  = [0,4.4,4.6,4.8,5,5.2,32.5,33.5,34.5]

# Currently not used parameters:
safety_gap          = 50
coup_gap            = 0.3

# Define library + cell:
lib = gdspy.GdsLibrary()
cell = lib.new_cell('RaceTrack')

# Start drawing:
dev_num = range(9)
path1 = gdspy.Path(width,(0,0))
for i in dev_num:
    # Bus
    x_start = path1.x
    y_start = path1.y
    path1.segment(700+(400*i),"+x", **ld_NWG)
    xbus = path1.x
    ybus = path1.y
    path1.turn(bend_radius,"l", **ld_NWG)
    path1.segment(275+(15*i), "+y", **ld_NWG)
    path1.turn(bend_radius,"r", **ld_NWG)
    path1.turn(bend_radius,"r", **ld_NWG)
    path1.segment(150, "-y", **ld_NWG)
    path1.turn(bend_radius,"l", **ld_NWG)
    x = path1.x
    y = path1.y
    path1.segment(Lc[i], "+x", **ld_NWG)
    path1.turn(bend_radius,"l", **ld_NWG)
    path1.segment(100+(5*i), "+y", **ld_NWG)
    path1.turn(bend_radius,"r", **ld_NWG)
    path1.segment(3300-(400*i)-Lc[i],"+x", **ld_NWG)
    x_end = path1.x
    path1.segment(chip_size - 2*taper_len - x_end, **ld_NWG)
    path1.segment(taper_len, final_width=final_taper_width, **ld_NWG)
    path3 = gdspy.Path(width, (x_start, y_start))
    path3.segment(taper_len, "-x", final_width=final_taper_width, **ld_NWG)
    
    #Ring
    path2 = gdspy.Path(width,(x+(Lc[i]/2),y-1-0.3))
    path2.segment(0.5*Lc[i], **ld_NWG)
    path2.turn(ring_radius,"r", **ld_NWG)
    path2.segment(race_track_len, "-y", **ld_NWG)
    path2.turn(ring_radius,"r", **ld_NWG)
    path2.segment(Lc[i], **ld_NWG)
    path2.turn(ring_radius,"r", **ld_NWG)
    path2.segment(race_track_len, "+y", **ld_NWG)
    x_ring = path2.x
    y_ring = path2.y
    path2.turn(ring_radius,"r", **ld_NWG)
    path2.segment(0.5*Lc[i], **ld_NWG)
    cell.add(path1)
    cell.add(path2)
    cell.add(path3)
    x = path2.x
    y = path2.y
    
    if i < N_rings_met:
        for j in range(N_stripes):
            path4 = gdspy.Path(1, (x_ring - size_stripes - stripes_gap + 2*j, y_ring))
            path4.segment(size_stripes, "-y", **ld_TNR)
            cell.add(path4)
    
    # path1 = gdspy.Path(1,(0,y-500))
    # path1 = gdspy.Path(1,(0,ybus-350))
    path1 = gdspy.Path(1,(0,y-300))
gdspy.LayoutViewer(lib)
if overwrite == 1:
    lib.write_gds('racetrack.gds')