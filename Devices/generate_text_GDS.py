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


txt1 = gdspy.Text("Lend = 19 um, L = 60.053",               Size, (0,0))
txt2 = gdspy.Text("Lend = 10 um, L = 69.835, 140nm diff",   Size, (0, 100))
txt3 = gdspy.Text("Lend = 10 um, L = 69.853, 200nm diff",   Size, (0, 200))
txt4 = gdspy.Text("Sweep W 330-470 nm",                     Size, (0, 300))
cell.add(txt1)
cell.add(txt2)
cell.add(txt3)
cell.add(txt4)

gdspy.LayoutViewer(lib)
if overwrite == 1:
    lib.write_gds("text_Inbar.gds")
    
gdspy.current_library = gdspy.GdsLibrary()