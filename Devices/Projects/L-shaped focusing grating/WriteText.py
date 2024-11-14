# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 11:15:46 2024

@author: benamis9
"""

import gdspy

# Create GDS library and cell
lib = gdspy.GdsLibrary()
cell = lib.new_cell('Text')

text1 = gdspy.Text("X = -4500 um, Y = 4500 um", 15, (-4500 - 170,  4500 + 65))
text2 = gdspy.Text("X = -4500 um, Y = -4500 um", 15, (-4500 - 170, -4500 + 65))
text3 = gdspy.Text("X = 4500 um, Y = -4500 um", 15, ( 4500 - 170, -4500 + 65))
text4 = gdspy.Text("X = 4500 um, Y = 4500 um", 15, ( 4500 - 170,  4500 + 65))
cell.add(text1).add(text2).add(text3).add(text4)

# Plot
gdspy.LayoutViewer(lib)

# Write to GDS file
lib.write_gds('Text.gds')

# Enable running on the same kernel
gdspy.current_library = gdspy.GdsLibrary()


