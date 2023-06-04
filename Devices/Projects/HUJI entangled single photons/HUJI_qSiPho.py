# -*- coding: utf-8 -*-
"""
Created on Tue May 30 15:00:43 2023

@author: slookma
"""

import gdspy

overwrite = 0 # 1 - Overwrite GDS, 0 - Don't overwrite
lib = gdspy.GdsLibrary()
cell = lib.new_cell('HUJI_couplers')

# Layers:
ld_Si          = {"layer": 50,    "datatype": 0}

# Parameters:
width               = 0.7       # 700 nm width
gap                 = 0.3       # 300 nm gap
radius              = 50        # bend of transition regions
Lend                = 10.4      # transition regions 
Lc                  = 32        # full power transfer distance
L_half              = Lc-Lend   # length for a 50:50 coupler
gapSafe             = 30        # distance between neighboring devices


# create U-shape




# x_run_start = (15*bend_radius + 2*Lc) * idx_row
# x_run_end   = (15*bend_radius + 2*Lc) * (2 - idx_row)
# ###########################################################################
# # Start path1 (bottom track)
# path1 = gdspy.Path(width, (taper_len, -idx_row*2*safety_gap - idx_col*(4*bend_radius + 3*coup_gap + 5*safety_gap)))
# x_start = path1.x
# y_start = path1.y
# path1.segment(x_run_start, "+x", **ld_NWG)
# path1.segment(2*bend_radius, **ld_NWG)
# # "Bump" for coupler
# path1.turn(bend_radius, "l", **ld_NWG)
# path1.turn(bend_radius, "r", **ld_NWG)
# path1.segment(Lc, **ld_NWG)
# x_coup1_bottom = path1.x
# y_coup1_bottom = path1.y
# path1.turn(bend_radius, "r", **ld_NWG)
# path1.turn(bend_radius, "l", **ld_NWG)
# # "Bump" for extra length
# path1.turn(bend_radius, "l", **ld_NWG)
# path1.turn(bend_radius, "r", **ld_NWG)
# x_middle = path1.x
# y_middle = path1.y
# path1.turn(bend_radius, "r", **ld_NWG)
# path1.turn(bend_radius, "l", **ld_NWG)
# # "Bump" for coupler
# path1.turn(bend_radius, "l", **ld_NWG)
# path1.turn(bend_radius, "r", **ld_NWG)
# path1.segment(Lc, **ld_NWG)
# x_coup2_bottom = path1.x
# y_coup2_bottom = path1.y
# path1.turn(bend_radius, "r", **ld_NWG)
# path1.turn(bend_radius, "l", **ld_NWG)
# # S shape
# path1.turn(bend_radius, "l", **ld_NWG)
# path1.segment(2*bend_radius + coup_gap - safety_gap, **ld_NWG)
# path1.turn(bend_radius, "r", **ld_NWG)
# path1.segment(x_run_end, **ld_NWG)
# x_end = path1.x
# path1.segment(chip_size - x_end - taper_len, **ld_NWG)
# path1.segment(taper_len, final_width=final_taper_width, **ld_NWG)
# path4 = gdspy.Path(width, (x_start, y_start))
# path4.segment(taper_len, "-x", final_width=final_taper_width, **ld_NWG)

# ###########################################################################
# # Start path2 + path3 (top track)
# path2 = gdspy.Path(width, (x_coup1_bottom, y_coup1_bottom + width + coup_gap))
# # Right half of the coupler "bump"
# path2.turn(bend_radius, "l", **ld_NWG)
# path2.turn(bend_radius, "r", **ld_NWG)
# # Straight section where bottom has "bump"
# path2.segment(4*bend_radius, **ld_NWG)
# # "Bump" for coupler
# path2.turn(bend_radius, "r", **ld_NWG)
# path2.turn(bend_radius, "l", **ld_NWG)
# path2.segment(Lc, **ld_NWG)
# path2.turn(bend_radius, "l", **ld_NWG)
# path2.turn(bend_radius, "r", **ld_NWG)
# # X run while bottom does S shape
# path2.segment(2*bend_radius, **ld_NWG)
# path2.segment(x_run_end, **ld_NWG)
# x_end = path2.x
# path2.segment(chip_size - x_end - taper_len, **ld_NWG)
# path2.segment(taper_len, final_width=final_taper_width, **ld_NWG)

# # Back to first coupler, going left
# path3 = gdspy.Path(width, (x_coup1_bottom, y_coup1_bottom + width + coup_gap))
# path3.segment(Lc, "-x", **ld_NWG)
# path3.turn(bend_radius, "r", **ld_NWG)
# path3.turn(bend_radius, "ll", **ld_NWG)
# path3.segment(2*bend_radius + coup_gap - safety_gap, **ld_NWG)
# path3.turn(bend_radius, "r", **ld_NWG)
# path3.segment(x_run_start, **ld_NWG)
# path3.segment(taper_len, final_width=final_taper_width, **ld_NWG)




cell.add(path1)                             # this part actually adds the polygon

gdspy.LayoutViewer(lib)
if overwrite == 1:
    lib.write_gds("HUJI_qSiPho.gds")
    

gdspy.current_library = gdspy.GdsLibrary()  # this line is to restart the console after every run

