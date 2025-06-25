# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 12:01:06 2025

@author: USER
"""

import numpy as np
import gdspy
import math


layer           = 50
datatype        = 0
LAYER           = {"layer": layer, "datatype": datatype}
overwrite       = 1 # 0 - Don't write GDS, 1 - Write GDS
period          = 0.900375
DC              = 0.5
gap             = 14.031
width           = period*DC
height          = 10
Nstripes        = math.floor(gap/period)
GC_coorX        = list([-3429.40,   #SWG11L
                        -384.631,   #SWG11R
                        570.60,     #SWG21L
                        3615.369,   #SWG21R
                        -3429.40,   #SWG12L
                        -384.631,   #SWG12R 
                        570.60,     #SWG22L
                        3615.369,   #SWG22R
                        -3629.4,    #Ring11L
                        -384.631,   #Ring11R
                        370.6,      #Ring21L
                        3615.369,   #Ring21R
                        -3629.4,    #Ring12L
                        -384.631,   #Ring12R
                        370.6,      #Ring22L
                        3615.369,   #Ring22R
                        -4562.4,    #LWG1
                        -4437.635,  #LWG1
                        -4487.824,  #LWG1
                        4340.554,   #LWG1
                        4340.369,   #LWG1
                        -4562.4,    #LWG2
                        -4437.635,  #LWG2
                        -4487.824,  #LWG2
                        4340.554,   #LWG2
                        4340.369,   #LWG2
                        -4562.4,    #LWG3
                        -4437.635,  #LWG3
                        -4487.824,  #LWG3
                        4340.554,   #LWG3
                        4340.369,   #LWG3
                        -4562.4,    #LWG4
                        -4437.635,  #LWG4
                        -4487.824,  #LWG4
                        4340.554,   #LWG4
                        4340.369,   #LWG4
                        -4487.4,    #LWG5
                        4465.554,   #LWG5
                        4465.369,   #LWG5
                        -4486.65,   #LWG6
                        4466.304,   #LWG6
                        4466.119,   #LWG6
                        -4487.4,    #LWG7
                        4465.554,   #LWG7
                        4465.369,   #LWG7
                        -4487.4,    #LWG8
                        4465.554,   #LWG8
                        4465.369    #LWG8
                        ])
GC_coorY        = list([4254.85,    #SWG11L
                        4254.85,    #SWG11R 
                        4254.85,    #SWG21L 
                        4254.85,    #SWG21R  
                        4004.85,    #SWG12L  
                        4004.85,    #SWG12R 
                        4004.85,    #SWG22L  
                        4004.85,    #SWG22R 
                        3504.85,    #Ring11L
                        3504.85,    #Ring11R
                        3504.85,    #Ring21L
                        3504.85,    #Ring21R
                        3004.85,    #Ring12L
                        3004.85,    #Ring12R
                        3004.85,    #Ring22L
                        3004.85,    #Ring22R
                        2004.85,    #LWG1
                        1601.793,   #LWG1
                        1501.266,   #LWG1
                        2206.006,   #LWG1
                        2004.85,    #LWG1
                        954.85,     #LWG2
                        551.793,    #LWG2
                        451.266,    #LWG2
                        1156.006,   #LWG2
                        954.85,     #LWG2
                        -95.15,     #LWG3
                        -498.207,   #LWG3
                        -598.734,   #LWG3
                        106.006,    #LWG3
                        -95.15,     #LWG3
                        -1145.15,   #LWG4
                        -1548.207,  #LWG4
                        -1648.734,  #LWG4
                        -943.994,   #LWG4
                        -1145.15,   #LWG4
                        -1995.15,   #LWG5
                        -1793.994,  #LWG5
                        -1995.15,   #LWG5
                        -2695.15,   #LWG6
                        -2493.994,  #LWG6
                        -2695.15,   #LWG6
                        -3395.15,   #LWG7
                        -3193.994,  #LWG7
                        -3395.15,   #LWG7
                        -4095.15,   #LWG8
                        -3893.994,  #LWG8
                        -4095.15    #LWG8
                        ])

# Create GDS library and cell
lib        = gdspy.GdsLibrary()
cell       = lib.new_cell('TowerSBS_GC')

for idxGC in range(len(GC_coorX)):
    for idxStripe in range(Nstripes):
        GCstripe = gdspy.Path(width, (GC_coorX[idxGC] + (idxStripe+1)*period, GC_coorY[idxGC]))
        GCstripe.segment(height, '-y', **LAYER)
        
        cell.add(GCstripe)
    

# Plot
gdspy.LayoutViewer(lib)

# Write to GDS file
if overwrite:
    lib.write_gds('TowerSBS_GC.gds')

# Enable running on the same kernel
gdspy.current_library = gdspy.GdsLibrary()














