# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 11:15:46 2024

@author: benamis9
"""

import gdspy
import numpy as np

lib = gdspy.GdsLibrary()
cell_text = lib.new_cell('text')

periods      = list(np.asarray(np.arange(-0.02, 0.025, 0.005)) + 0.550)
DCs          = list([0.5])
vertical_gap = 200
text_size    = 40

for idx_DC, DC in enumerate(DCs):
    for idx_per, period in enumerate(periods):
        X = -3500
        Y = -vertical_gap*(idx_DC*len(periods) + idx_per)
        htext = gdspy.Text("DC = " + str(DC) + "%, Period = " + str(round(period*1000)) + "nm", text_size, (X,Y))
        cell_text.add(htext)
        
        X = -3500 + 6100
        Y = 100 - vertical_gap*(idx_DC*len(periods) + idx_per)
        htext = gdspy.Text("DC = " + str(DC) + "%, Period = " + str(round(period*1000)) + "nm", text_size, (X,Y))
        cell_text.add(htext)
        
htext = gdspy.Text("X = -3300, Y = 1700", text_size, (-3300 - 330,  1700 + 80))
cell_text.add(htext)
htext = gdspy.Text("X = 3300, Y = 1700", text_size, ( 3300 - 330,  1700 + 80))
cell_text.add(htext)
htext = gdspy.Text("X = -3300, Y = -2100", text_size, (-3300 - 330, -2100 + 80))
cell_text.add(htext)
htext = gdspy.Text("X = 3300, Y = -2100", text_size, ( 3300 - 330, -2100 + 80))
cell_text.add(htext)

htext = gdspy.Text("L = " + str(5) + "um", text_size, (6000,0))
cell_text.add(htext)
htext = gdspy.Text("L = " + str(6) + "um", text_size, (6000,-200))
cell_text.add(htext)
htext = gdspy.Text("L = " + str(7) + "um", text_size, (6000,-400))
cell_text.add(htext)
htext = gdspy.Text("L = " + str(8) + "um", text_size, (6000,-600))
cell_text.add(htext)
htext = gdspy.Text("L = " + str(5) + "um", text_size, (8500,400))
cell_text.add(htext)
htext = gdspy.Text("L = " + str(6) + "um", text_size, (8500,200))
cell_text.add(htext)
htext = gdspy.Text("L = " + str(7) + "um", text_size, (8500,0))
cell_text.add(htext)
htext = gdspy.Text("L = " + str(8) + "um", text_size, (8500,-200))
cell_text.add(htext)
htext = gdspy.Text("L = " + str(5) + "um", text_size, (9200,0))
cell_text.add(htext)
htext = gdspy.Text("L = " + str(6) + "um", text_size, (9200,-200))
cell_text.add(htext)
htext = gdspy.Text("L = " + str(7) + "um", text_size, (9200,-400))
cell_text.add(htext)
htext = gdspy.Text("L = " + str(8) + "um", text_size, (9200,-600))
cell_text.add(htext)
htext = gdspy.Text("L = " + str(5) + "um", text_size, (11700,400))
cell_text.add(htext)
htext = gdspy.Text("L = " + str(6) + "um", text_size, (11700,200))
cell_text.add(htext)
htext = gdspy.Text("L = " + str(7) + "um", text_size, (11700,0))
cell_text.add(htext)
htext = gdspy.Text("L = " + str(8) + "um", text_size, (11700,-200))
cell_text.add(htext)

# Plot
gdspy.LayoutViewer(lib)

# Write to GDS file
lib.write_gds('Text.gds')

# Enable running on the same kernel
gdspy.current_library = gdspy.GdsLibrary()


