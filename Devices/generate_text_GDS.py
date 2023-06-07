# -*- coding: utf-8 -*-
"""
Created on Wed May 24 22:51:00 2023

@author: benamis9
"""


# Units: um

import gdspy
import math


overwrite = 1 # 1 - Overwrite GDS, 0 - Don't overwrite
lib = gdspy.GdsLibrary()
cell = lib.new_cell('Text')
Size = 50


txt1 = gdspy.Text("1064nm",               Size, (0,0))
txt2 = gdspy.Text("MZI Lc 0,5,10,15,20,25.30,35, 40, 45, 50, 55, 60,70,80,90,100,110,110,120",   Size, (0, 100))
txt3 = gdspy.Text("Racetrack 0,2,4,6,8,10,12,14,16",   Size, (0, 200))
txt4 = gdspy.Text("Sweep W 330-470 nm",                     Size, (0, 300))
cell.add(txt1)
cell.add(txt2)
cell.add(txt3)
cell.add(txt4)

gdspy.LayoutViewer(lib)
if overwrite == 1:
    lib.write_gds("text_1064nm.gds")
    
gdspy.current_library = gdspy.GdsLibrary()