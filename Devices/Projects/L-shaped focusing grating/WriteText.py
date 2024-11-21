# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 11:15:46 2024

@author: benamis9
"""

import gdspy
import numpy as np

lib = gdspy.GdsLibrary()
cell_text = lib.new_cell('text')

periods      = list(np.asarray(np.arange(-0.02, 0.025, 0.005)) + 0.540)
DCs          = list([50, 60])
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
        
htext = gdspy.Text("X = -4000, Y = 4000", text_size, (-4000 - 330,  4000 + 80))
cell_text.add(htext)
htext = gdspy.Text("X = 4000, Y = 4000", text_size, ( 4000 - 330,  4000 + 80))
cell_text.add(htext)
htext = gdspy.Text("X = -4000, Y = -4000", text_size, (-4000 - 330, -4000 + 80))
cell_text.add(htext)
htext = gdspy.Text("X = 4000, Y = -4000", text_size, ( 4000 - 330, -4000 + 80))
cell_text.add(htext)

# Plot
gdspy.LayoutViewer(lib)

# Write to GDS file
lib.write_gds('Text.gds')

# Enable running on the same kernel
gdspy.current_library = gdspy.GdsLibrary()


