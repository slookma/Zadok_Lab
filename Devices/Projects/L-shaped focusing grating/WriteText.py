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
lengths      = list([5,6,7,8])
vertical_gap = 200
text_size    = 40
Xmarkers     = list([3500, -3500, -3500,  3500])
Ymarkers     = list([3000,  3000, -3000, -3000])


for idx_DC, DC in enumerate(DCs):
    for idx_per, period in enumerate(periods):
        X = -3500
        Y = -vertical_gap*(idx_DC*len(periods) + idx_per)
        # htext = gdspy.Text("DC = " + str(DC) + "%, Period = " + str(round(period*1000)) + "nm", text_size, (X,Y))
        htext = gdspy.Text("Per " + str(round(period*1000)) + "nm", text_size, (X,Y))
        cell_text.add(htext)
        
        X = -3500 + 5600
        Y = 100 - vertical_gap*(idx_DC*len(periods) + idx_per)
        # htext = gdspy.Text("DC = " + str(DC) + "%, Period = " + str(round(period*1000)) + "nm", text_size, (X,Y))
        htext = gdspy.Text("Per " + str(round(period*1000)) + "nm", text_size, (X,Y))
        cell_text.add(htext)
        

for idx_mkr, (X,Y) in enumerate(zip(Xmarkers, Ymarkers)):
    htext = gdspy.Text("X = " + str(X) + ", Y = " + str(Y), text_size, (X - 330,  Y + 80))
    cell_text.add(htext)


for idx_L, L in enumerate(lengths):
    htext = gdspy.Text("L = " + str(L) + "um", text_size, (6000, -200 * idx_L))
    cell_text.add(htext)
    htext = gdspy.Text("L = " + str(L) + "um", text_size, (8500, 400 - 200 * idx_L))
    cell_text.add(htext)
    htext = gdspy.Text("L = " + str(L) + "um", text_size, (9200, -200 * idx_L))
    cell_text.add(htext)
    htext = gdspy.Text("L = " + str(L) + "um", text_size, (11700, 400 - 200 * idx_L))
    cell_text.add(htext)

# Plot
gdspy.LayoutViewer(lib)

# Write to GDS file
lib.write_gds('Text.gds')

# Enable running on the same kernel
gdspy.current_library = gdspy.GdsLibrary()


