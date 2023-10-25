# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Units: um

import numpy
import gdspy


# lib = gdspy.GdsLibrary()
# cell = lib.new_cell('via_array')

def via_array(cell, via_type, via_locX, via_locY, rows, columns, via_side, via_spacing, side_gap):
    
    # Layers:
    ld_NWG          = {"layer": 174,    "datatype": 0}
    ld_Silox        = {"layer": 9,      "datatype": 0}
    ld_taperMark    = {"layer": 118,    "datatype": 120}
    ld_GC           = {"layer": 118,    "datatype": 121}
    ld_SUS          = {"layer": 195,    "datatype": 0}
    ld_VG1          = {"layer": 192,    "datatype": 0}
    ld_TNR          = {"layer": 26,     "datatype": 0}
    ld_Contact      = {"layer": 7,      "datatype": 0}
    ld_VIA1         = {"layer": 17,     "datatype": 0}
    ld_METAL1       = {"layer": 8,      "datatype": 0}
    ld_METAL2       = {"layer": 18,     "datatype": 0}
    ld_dataExtend   = {"layer": 118,    "datatype": 134}
    
    
    if via_type == "Contact":
        bottom_rect = gdspy.Rectangle((via_locX, via_locY), (via_locX + columns*via_side + (columns - 1)*via_spacing + 2*side_gap, via_locY + rows*via_side + (rows - 1)*via_spacing + 2*side_gap), **ld_TNR)
        top_rect    = gdspy.Rectangle((via_locX, via_locY), (via_locX + columns*via_side + (columns - 1)*via_spacing + 2*side_gap, via_locY + rows*via_side + (rows - 1)*via_spacing + 2*side_gap), **ld_METAL1)
    elif via_type == "VIA1":
        bottom_rect = gdspy.Rectangle((via_locX, via_locY), (via_locX + columns*via_side + (columns - 1)*via_spacing + 2*side_gap, via_locY + columns*via_side + (columns - 1)*via_spacing + 2*side_gap), **ld_METAL1)
        top_rect    = gdspy.Rectangle((via_locX, via_locY), (via_locX + columns*via_side + (columns - 1)*via_spacing + 2*side_gap, via_locY + columns*via_side + (columns - 1)*via_spacing + 2*side_gap), **ld_METAL2)
    
    cell.add(bottom_rect)
    cell.add(top_rect)
    
    for row_idx in range(rows):
        for col_idx in range(columns):
            point1 = (via_locX + side_gap + col_idx*(via_side + via_spacing)           , via_locY + side_gap + row_idx*(via_side + via_spacing))
            point2 = (via_locX + side_gap + col_idx*(via_side + via_spacing) + via_side, via_locY + side_gap + row_idx*(via_side + via_spacing) + via_side)
            if via_type == "Contact":
                via = gdspy.Rectangle(point1, point2, **ld_Contact)
            elif via_type == "VIA1":
                via = gdspy.Rectangle(point1, point2, **ld_VIA1)
            cell.add(via)







