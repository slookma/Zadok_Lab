# -*- coding: utf-8 -*-
"""
Created on Wed May 24 22:51:00 2023

@author: benamis9
"""


# Units: um

import numpy
import gdspy


if __name__ == "__main__":
    lib = gdspy.GdsLibrary()
    cell = lib.new_cell('MZI_array')
    
    width               = 1
    taper_len           = 200
    final_taper_width   = 0.3
    bend_radius         = 90
    safety_gap          = 30
    coup_gap            = 0.3
    Lc_vec              = [0,6,8,10,11.85,14,24,26,28]
    chip_size           = 5000
    
    
    for idx_col in range(3):
        
        for idx_row in range(3):
            Lc = Lc_vec[idx_row + idx_col*3]
            x_run_start = (16*bend_radius + 2*Lc) * idx_row
            x_run_end   = (16*bend_radius + 2*Lc) * (2 - idx_row)
            ###########################################################################
            # Start path1 (bottom track)
            path1 = gdspy.Path(width, (taper_len, -idx_row*2*safety_gap - idx_col*(4*bend_radius + 3*coup_gap + 5*safety_gap)))
            x_start = path1.x
            y_start = path1.y
            path1.segment(x_run_start, "+x")
            path1.segment(2*bend_radius)
            # "Bump" for coupler
            path1.turn(bend_radius, "l")
            path1.turn(bend_radius, "r")
            path1.segment(Lc)
            x_coup1_bottom = path1.x
            y_coup1_bottom = path1.y
            path1.turn(bend_radius, "r")
            path1.turn(bend_radius, "l")
            # "Bump" for extra length
            path1.turn(bend_radius, "l")
            path1.turn(bend_radius, "r")
            x_middle = path1.x
            y_middle = path1.y
            path1.turn(bend_radius, "r")
            path1.turn(bend_radius, "l")
            # "Bump" for coupler
            path1.turn(bend_radius, "l")
            path1.turn(bend_radius, "r")
            path1.segment(Lc)
            x_coup2_bottom = path1.x
            y_coup2_bottom = path1.y
            path1.turn(bend_radius, "r")
            path1.turn(bend_radius, "l")
            # S shape
            path1.turn(bend_radius, "l")
            path1.segment(2*bend_radius + coup_gap - safety_gap)
            path1.turn(bend_radius, "r")
            path1.segment(x_run_end)
            x_end = path1.x
            path1.segment(chip_size - x_end - taper_len)
            path1.segment(taper_len, final_width=final_taper_width)
            path4 = gdspy.Path(width, (x_start, y_start))
            path4.segment(taper_len, "-x", final_width=final_taper_width)
            
            ###########################################################################
            # Start path2 + path3 (top track)
            path2 = gdspy.Path(width, (x_coup1_bottom, y_coup1_bottom + width + coup_gap))
            # Right half of the coupler "bump"
            path2.turn(bend_radius, "l")
            path2.turn(bend_radius, "r")
            # Straight section where bottom has "bump"
            path2.segment(4*bend_radius)
            # "Bump" for coupler
            path2.turn(bend_radius, "r")
            path2.turn(bend_radius, "l")
            path2.segment(Lc)
            path2.turn(bend_radius, "l")
            path2.turn(bend_radius, "r")
            # X run while bottom does S shape
            path2.segment(2*bend_radius)
            path2.segment(x_run_end)
            x_end = path2.x
            path2.segment(chip_size - x_end - taper_len)
            path2.segment(taper_len, final_width=final_taper_width)
            
            # Back to first coupler, going left
            path3 = gdspy.Path(width, (x_coup1_bottom, y_coup1_bottom + width + coup_gap))
            path3.segment(Lc, "-x")
            path3.turn(bend_radius, "r")
            path3.turn(bend_radius, "ll")
            path3.segment(2*bend_radius + coup_gap - safety_gap)
            path3.turn(bend_radius, "r")
            path3.segment(x_run_start)
            path3.segment(taper_len, final_width=final_taper_width)
            
            
            
            # txt = gdspy.Text("Lc = " + str(Lc) + " um", bend_radius/5, (x_middle-bend_radius/2, y_middle + bend_radius), layer=2)
            
            cell.add(path1)
            cell.add(path2)
            cell.add(path3)
            cell.add(path4)
            # cell.add(txt)
    
    
    # box = gdspy.Path(width/10, (0,450))
    # box.segment(5000, "+x", layer=1)
    # box.segment(5000, "-y", layer=1)
    # box.segment(5000, "-x", layer=1)
    # box.segment(5000, "+y", layer=1)
    # cell.add(box)
    
    gdspy.LayoutViewer(lib)
    lib.write_gds("MZI1.gds")