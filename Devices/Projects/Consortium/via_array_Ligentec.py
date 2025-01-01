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

def via_array_Ligentec(cell, via_type, via_locX, via_locY, rows, columns, via_side, via_spacing, side_gap):
    
    # Layers:
    ld_NWG          = {"layer": 2,      "datatype": 0}
    ld_Silox        = {"layer": 33,     "datatype": 0}
    ld_HTR          = {"layer": 30,     "datatype": 0}
    ld_Contact      = {"layer": 31,      "datatype": 0}
    ld_METAL1       = {"layer": 32,      "datatype": 0}
    
    bottom_rect = gdspy.Rectangle((via_locX, via_locY), (via_locX + columns*via_side + (columns - 1)*via_spacing + 2*side_gap, via_locY + rows*via_side + (rows - 1)*via_spacing + 2*side_gap), **ld_HTR)
    top_rect    = gdspy.Rectangle((via_locX, via_locY), (via_locX + columns*via_side + (columns - 1)*via_spacing + 2*side_gap, via_locY + rows*via_side + (rows - 1)*via_spacing + 2*side_gap), **ld_METAL1)
    
    cell.add(bottom_rect)
    cell.add(top_rect)
    
    for row_idx in range(rows):
        for col_idx in range(columns):
            point1 = (via_locX + side_gap + col_idx*(via_side + via_spacing)           , via_locY + side_gap + row_idx*(via_side + via_spacing))
            point2 = (via_locX + side_gap + col_idx*(via_side + via_spacing) + via_side, via_locY + side_gap + row_idx*(via_side + via_spacing) + via_side)
            via = gdspy.Rectangle(point1, point2, **ld_Contact)
            cell.add(via)