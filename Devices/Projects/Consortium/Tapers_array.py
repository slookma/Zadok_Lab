# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 00:19:33 2023

@author: benamis9
"""
# Units: um

import numpy
import gdspy

overwrite = 0 # 1 - Overwrite GDS, 0 - Don't overwrite
lib = gdspy.GdsLibrary()
cell = lib.new_cell('Tapers_array')


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
width                   = 1
taper_len               = 190
N_tapers                = 50
s_bend_width            = 30
tapers_spacing          = 10
right_end               = 5000 - taper_len - 10
final_taper_width_vec   = numpy.linspace(0.1, 1, N_tapers)

for idx in range(N_tapers):
    # Sweep parameters
    final_taper_width = final_taper_width_vec[idx]
    
    
    #######################################################################
    # Start path1
    path1 = gdspy.Path(width, (10 + taper_len, -idx*tapers_spacing))
    path1.segment(taper_len, "-x", final_width=final_taper_width, **ld_NWG)
    
    #######################################################################
    # Start path2
    path2 = gdspy.Path(width, (right_end, -idx*tapers_spacing - s_bend_width))
    path2.segment(taper_len, "+x", final_width=final_taper_width, **ld_NWG)
        
    #######################################################################
    # Add all paths
    cell.add(path1)
    cell.add(path2)

gdspy.LayoutViewer(lib)
if overwrite == 1:
    lib.write_gds("Tapers_array.gds")

gdspy.current_library = gdspy.GdsLibrary()