# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Units: um

import numpy
import gdspy
from via_array import via_array

overwrite = 0 # 1 - Overwrite GDS, 0 - Don't overwrite
lib = gdspy.GdsLibrary()
cell = lib.new_cell('Elliptical_Filter2')


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

# Parameters:
width               = 1
width_TNR           = 2*width
width_M1            = 5*width
width_M2            = 20*width
taper_len           = 200
final_taper_width   = 0.3    
bend_radius         = 80
ring_radius         = 100
safety_gap          = 30
coup_gap            = 0.3
run_x_start         = 2*bend_radius + safety_gap
vertical_50_coup    = safety_gap/2 + ring_radius - bend_radius
vertical_out_coup   = 2 * bend_radius + coup_gap
Lc_50_coup          = 10
side_M2             = 100
side_silox          = 80
pad_shift_const     = 127
TNR_tail            = 20
# Lc_D3_vec           = [4.95, 14.15, 10.75, 19.95]
# Lc_D4_vec           = [9.65, 18.85, 6.81, 15.9]
# Lc_D3_vec           = [4.95,  6,  7,  8,  9, 10, 11, 12, 14.15]
# Lc_D4_vec           = [9.65, 11, 12, 13, 14, 15, 16, 17, 18.85]
Lc_D3_vec           = [4.95,  6.5,  7.5,  9.0, 10.0, 11.5, 12.5, 14.15]
Lc_D4_vec           = [9.65, 11.0, 12.5, 13.5, 15.0, 16.0, 17.5, 18.85]
run_x_through_coup  = 7 * bend_radius + Lc_50_coup
right_end           = 5000 - taper_len - 10 - 10


for idx in range(len(Lc_D3_vec)):
    # Sweep parameters
    Lc_D3 = Lc_D3_vec[idx]
    Lc_D4 = Lc_D4_vec[idx]
    run_x_through_ring1 = 3 * bend_radius + Lc_D3
    run_x_through_ring2 = 3 * bend_radius + Lc_D4
    
    
    #######################################################################
    # Start path1 (bottom track)
    path1 = gdspy.Path(width, (taper_len, -idx * (4*bend_radius + 2*vertical_50_coup + 4*safety_gap + coup_gap)))
    x_start = path1.x
    y_start = path1.y
    path1.segment(run_x_start, "+x", **ld_NWG)
    # "Bump" for coupler
    path1.turn(bend_radius, "l", **ld_NWG)
    path1.segment(vertical_50_coup, **ld_NWG)
    path1.turn(bend_radius, "r", **ld_NWG)
    path1.segment(Lc_50_coup, **ld_NWG)
    x_50_coup1 = path1.x
    y_50_coup1 = path1.y
    path1.turn(bend_radius, "r", **ld_NWG)
    path1.segment(vertical_50_coup, **ld_NWG)
    path1.turn(bend_radius, "l", **ld_NWG)
    # Run through ring in the other arm
    path1.segment(run_x_through_ring1, **ld_NWG)
    # "Bump" for ring
    path1.turn(bend_radius, "l", **ld_NWG)
    path1.turn(bend_radius, "r", **ld_NWG)
    path1.segment(Lc_D3, **ld_NWG)
    x_ring1_bottom = path1.x
    y_ring1_bottom = path1.y
    path1.turn(bend_radius, "r", **ld_NWG)
    path1.turn(bend_radius, "l", **ld_NWG)
    # Run through coupler in the other arm
    path1.segment(run_x_through_coup, **ld_NWG)
    # Double "bump" for coupler
    path1.turn(bend_radius, "l", **ld_NWG)
    path1.segment(vertical_out_coup, **ld_NWG)
    path1.turn(bend_radius, "rr", **ld_NWG)
    path1.turn(bend_radius, "l", **ld_NWG)
    path1.segment(Lc_50_coup, **ld_NWG)
    x_out_coup_bottom = path1.x
    y_out_coup_bottom = path1.y
    path1.turn(bend_radius, "l", **ld_NWG)
    path1.turn(bend_radius, "rr", **ld_NWG)
    path1.segment(vertical_out_coup, **ld_NWG)
    MZI_TNR_cover_x = path1.x
    MZI_TNR_cover_y = path1.y
    path1.turn(bend_radius, "l", **ld_NWG)
    # Run through ring in the other arm
    path1.segment(run_x_through_ring2, **ld_NWG)
    # "Bump" for ring
    path1.turn(bend_radius, "l", **ld_NWG)
    path1.turn(bend_radius, "r", **ld_NWG)
    path1.segment(Lc_D4, **ld_NWG)
    x_ring2_bottom = path1.x
    y_ring2_bottom = path1.y
    path1.turn(bend_radius, "r", **ld_NWG)
    path1.turn(bend_radius, "l", **ld_NWG)
    # "Bump" for coupler
    path1.turn(bend_radius, "l", **ld_NWG)
    path1.segment(vertical_50_coup, **ld_NWG)
    path1.turn(bend_radius, "r", **ld_NWG)
    path1.segment(Lc_50_coup, **ld_NWG)
    x_50_coup2_bottom = path1.x
    y_50_coup2_bottom = path1.y
    path1.turn(bend_radius, "r", **ld_NWG)
    path1.segment(vertical_50_coup, **ld_NWG)
    # Turn to create S shape
    path1.turn(bend_radius, "ll", **ld_NWG)
    path1.segment(2*bend_radius + coup_gap + 2*vertical_50_coup - safety_gap, **ld_NWG)
    path1.turn(bend_radius, "r", **ld_NWG)
    # Continue a bit to align all
    path1.segment(right_end - path1.x, **ld_NWG)
    # Add tapers at both ends
    path1.segment(taper_len, final_width=final_taper_width, **ld_NWG)
    start_taper = gdspy.Path(width, (x_start, y_start))
    start_taper.segment(taper_len, "-x", final_width=final_taper_width, **ld_NWG)
    
    #######################################################################
    # Start path2 + path3 (bottom WG couples to bottom track)
    path2 = gdspy.Path(width, (x_out_coup_bottom, y_out_coup_bottom - coup_gap - width))
    path2.turn(bend_radius, "r", **ld_NWG)
    path2.segment(coup_gap + safety_gap, **ld_NWG)
    path2.turn(bend_radius, "l", **ld_NWG)
    path2.segment(12*bend_radius + 2*Lc_D4 + Lc_50_coup, **ld_NWG)
    # Turn to create S shape
    path2.segment(bend_radius + safety_gap, **ld_NWG)
    path2.turn(bend_radius, "l", **ld_NWG)
    path2.segment(2*bend_radius + coup_gap + 2*vertical_50_coup - safety_gap, **ld_NWG)
    path2.turn(bend_radius, "r", **ld_NWG)
    # Continue a bit to align all
    path2.segment(right_end - path2.x, **ld_NWG)
    # Add taper
    path2.segment(taper_len, final_width=final_taper_width, **ld_NWG)
    
    path3 = gdspy.Path(width, (x_out_coup_bottom, y_out_coup_bottom - coup_gap - width))
    path3.segment(Lc_50_coup, "-x", **ld_NWG)
    path3.turn(bend_radius, "l", **ld_NWG)
    path3.segment(coup_gap + safety_gap, **ld_NWG)
    path3.turn(bend_radius, "r", **ld_NWG)
    path3.segment(20*bend_radius + 2*Lc_D3 + 2*Lc_50_coup + run_x_start, **ld_NWG)
    path3.segment(taper_len, final_width=final_taper_width, **ld_NWG)
    
    #######################################################################
    # Start path4 + path5 (Upper track) from the rightmost 50 coupler
    path4 = gdspy.Path(width, (x_50_coup2_bottom, y_50_coup2_bottom + coup_gap + width))
    # Complete left part of the "bump"
    path4.segment(Lc_50_coup, "-x", **ld_NWG)
    path4.turn(bend_radius, "r", **ld_NWG)
    path4.segment(vertical_50_coup, **ld_NWG)
    path4.turn(bend_radius, "l", **ld_NWG)
    # Run through ring in the other arm
    path4.segment(run_x_through_ring1, **ld_NWG)
    # "Bump" for ring
    path4.turn(bend_radius, "l", **ld_NWG)
    path4.turn(bend_radius, "r", **ld_NWG)
    x_ring2_top = path4.x
    y_ring2_top = path4.y
    path4.segment(Lc_D4, **ld_NWG)
    path4.turn(bend_radius, "r", **ld_NWG)
    path4.turn(bend_radius, "l", **ld_NWG)
    # Run through coupler in the other arm
    path4.segment(run_x_through_coup, **ld_NWG)
    # Double "bump" for coupler
    path4.turn(bend_radius, "l", **ld_NWG)
    path4.segment(vertical_out_coup, **ld_NWG)
    path4.turn(bend_radius, "rr", **ld_NWG)
    path4.turn(bend_radius, "l", **ld_NWG)
    x_out_coup_top = path4.x
    y_out_coup_top = path4.y
    path4.segment(Lc_50_coup, **ld_NWG)
    path4.turn(bend_radius, "l", **ld_NWG)
    path4.turn(bend_radius, "rr", **ld_NWG)
    path4.segment(vertical_out_coup, **ld_NWG)
    path4.turn(bend_radius, "l", **ld_NWG)
    # Run through ring in the other arm
    path4.segment(run_x_through_ring2, **ld_NWG)
    # "Bump" for ring
    path4.turn(bend_radius, "l", **ld_NWG)
    path4.turn(bend_radius, "r", **ld_NWG)
    x_ring1_top = path4.x
    y_ring1_top = path4.y
    path4.segment(Lc_D3, **ld_NWG)
    path4.turn(bend_radius, "r", **ld_NWG)
    path4.turn(bend_radius, "l", **ld_NWG)
    # "Bump" for coupler
    path4.turn(bend_radius, "l", **ld_NWG)
    path4.segment(vertical_50_coup, **ld_NWG)
    path4.turn(bend_radius, "r", **ld_NWG)
    path4.segment(Lc_50_coup, **ld_NWG)
    path4.turn(bend_radius, "r", **ld_NWG)
    path4.segment(vertical_50_coup, **ld_NWG)
    # Turn to create S shape
    path4.turn(bend_radius, "ll", **ld_NWG)
    path4.segment(2*bend_radius + coup_gap + 2*vertical_50_coup - safety_gap, **ld_NWG)
    path4.turn(bend_radius, "r", **ld_NWG)
    path4.segment(run_x_start - 2*bend_radius, **ld_NWG)
    # Add taper
    path4.segment(taper_len, final_width=final_taper_width, **ld_NWG)
    
    # Complete right part of the "bump" for the right 50 coupler
    path5 = gdspy.Path(width, (x_50_coup2_bottom, y_50_coup2_bottom + coup_gap + width))
    # Complete right part of the "bump"
    path5.turn(bend_radius, "l", **ld_NWG)
    path5.segment(vertical_50_coup, **ld_NWG)
    path5.turn(bend_radius, "r", **ld_NWG)
    # Continue a bit to align all
    path5.segment(right_end - path5.x, **ld_NWG)
    # Add taper
    path5.segment(taper_len, final_width=final_taper_width, **ld_NWG)
    
    
    #######################################################################
    # Start path6 + path7 (top WG couples to top track)
    path6 = gdspy.Path(width, (x_out_coup_top, y_out_coup_top + coup_gap + width))
    path6.segment(Lc_50_coup, "-x", **ld_NWG)
    path6.turn(bend_radius, "r", **ld_NWG)
    path6.segment(coup_gap + safety_gap, **ld_NWG)
    path6.turn(bend_radius, "l", **ld_NWG)
    path6.segment(13*bend_radius + Lc_D3 + Lc_D4 + Lc_50_coup + safety_gap, **ld_NWG)
    path6.turn(bend_radius, "l", **ld_NWG)
    path6.segment(2*bend_radius + coup_gap + 2*vertical_50_coup - safety_gap, **ld_NWG)
    path6.turn(bend_radius, "r", **ld_NWG)
    # Add taper
    path6.segment(taper_len, final_width=final_taper_width, **ld_NWG)
    
    path7 = gdspy.Path(width, (x_out_coup_top, y_out_coup_top + coup_gap + width))
    path7.turn(bend_radius, "l", **ld_NWG)
    path7.segment(coup_gap + safety_gap, **ld_NWG)
    path7.turn(bend_radius, "r", **ld_NWG)
    path7.segment(20*bend_radius + Lc_D3 + Lc_D4 + 2*Lc_50_coup, **ld_NWG)
    # Continue a bit to align all
    path7.segment(right_end - path7.x, **ld_NWG)
    # Add taper
    path7.segment(taper_len, final_width=final_taper_width, **ld_NWG)
    
    
    #######################################################################
    # Start path8+path12 (ring1 bottom) - NWG + TNR cover
    path8 = gdspy.Path(width, (x_ring1_bottom, y_ring1_bottom + coup_gap + width))
    path8.turn(ring_radius, "ll", **ld_NWG)
    path8.segment(Lc_D3, **ld_NWG)
    path8.turn(ring_radius, "ll", **ld_NWG)
    path8.segment(Lc_D3, **ld_NWG)
    
    path12 = gdspy.Path(width_TNR, (x_ring1_bottom + ring_radius, y_ring1_bottom + ring_radius + coup_gap + width))
    path12.segment(0, '+y', **ld_TNR)
    x_ring1_bottom_TNR1 = path12.x
    y_ring1_bottom_TNR1 = path12.y
    path12.turn(ring_radius, "l", **ld_TNR)
    path12.segment(Lc_D3, **ld_TNR)
    path12.turn(ring_radius, "l", **ld_TNR)
    x_ring1_bottom_TNR2 = path12.x
    y_ring1_bottom_TNR2 = path12.y
    
    #######################################################################
    # Start path9+path13 (ring2 bottom) - NWG + TNR cover
    path9 = gdspy.Path(width, (x_ring2_bottom, y_ring2_bottom + coup_gap + width))
    path9.turn(ring_radius, "ll", **ld_NWG)
    path9.segment(Lc_D4, **ld_NWG)
    path9.turn(ring_radius, "ll", **ld_NWG)
    path9.segment(Lc_D4, **ld_NWG)
    
    path13 = gdspy.Path(width_TNR, (x_ring2_bottom + ring_radius, y_ring2_bottom + ring_radius + coup_gap + width))
    path13.segment(0, '+y', **ld_TNR)
    x_ring2_bottom_TNR1 = path13.x
    y_ring2_bottom_TNR1 = path13.y
    path13.turn(ring_radius, "l", **ld_TNR)
    path13.segment(Lc_D4, **ld_TNR)
    path13.turn(ring_radius, "l", **ld_TNR)
    x_ring2_bottom_TNR2 = path13.x
    y_ring2_bottom_TNR2 = path13.y
    
    #######################################################################
    # Start path10+path14 (ring1 top) - NWG + TNR cover
    path10 = gdspy.Path(width, (x_ring1_top, y_ring1_top - coup_gap - width))
    path10.turn(ring_radius, "rr", **ld_NWG)
    path10.segment(Lc_D3, **ld_NWG)
    path10.turn(ring_radius, "rr", **ld_NWG)
    path10.segment(Lc_D3, **ld_NWG)
    
    path14 = gdspy.Path(width_TNR, (x_ring1_top + ring_radius, y_ring1_top - ring_radius - coup_gap - width))
    path14.segment(0, '-y', **ld_TNR)
    x_ring1_top_TNR1 = path14.x
    y_ring1_top_TNR1 = path14.y
    path14.turn(ring_radius, "r", **ld_TNR)
    path14.segment(Lc_D3, **ld_TNR)
    path14.turn(ring_radius, "r", **ld_TNR)
    x_ring1_top_TNR2 = path14.x
    y_ring1_top_TNR2 = path14.y
    
    #######################################################################
    # Start path11+path15 (ring2 top) - NWG + TNR cover
    path11 = gdspy.Path(width, (x_ring2_top, y_ring2_top - coup_gap - width))
    path11.turn(ring_radius, "rr", **ld_NWG)
    path11.segment(Lc_D4, **ld_NWG)
    path11.turn(ring_radius, "rr", **ld_NWG)
    path11.segment(Lc_D4, **ld_NWG)
    
    path15 = gdspy.Path(width_TNR, (x_ring2_top + ring_radius, y_ring2_top - ring_radius - coup_gap - width))
    path15.segment(0, '-y', **ld_TNR)
    x_ring2_top_TNR1 = path15.x
    y_ring2_top_TNR1 = path15.y
    path15.turn(ring_radius, "r", **ld_TNR)
    path15.segment(Lc_D4, **ld_TNR)
    path15.turn(ring_radius, "r", **ld_TNR)
    x_ring2_top_TNR2 = path15.x
    y_ring2_top_TNR2 = path15.y

    #######################################################################
    # TNR extensions from rings
    path16 = gdspy.Path(width_TNR, (x_ring1_bottom_TNR1 - width, y_ring1_bottom_TNR1 + width))
    path16.segment(TNR_tail, '+x', **ld_TNR)
    
    path17 = gdspy.Path(width_TNR, (x_ring1_bottom_TNR2 + width, y_ring1_bottom_TNR2 + width))
    path17.segment(TNR_tail, '-x', **ld_TNR)
    
    path18 = gdspy.Path(width_TNR, (x_ring2_bottom_TNR1 - width, y_ring2_bottom_TNR1 + width))
    path18.segment(TNR_tail, '+x', **ld_TNR)
    
    path19 = gdspy.Path(width_TNR, (x_ring2_bottom_TNR2 + width, y_ring2_bottom_TNR2 + width))
    path19.segment(TNR_tail, '-x', **ld_TNR)
    
    path20 = gdspy.Path(width_TNR, (x_ring1_top_TNR1 - width, y_ring1_top_TNR1 - width))
    path20.segment(TNR_tail, '+x', **ld_TNR)
    
    path21 = gdspy.Path(width_TNR, (x_ring1_top_TNR2 + width, y_ring1_top_TNR2 - width))
    path21.segment(TNR_tail, '-x', **ld_TNR)
    
    path22 = gdspy.Path(width_TNR, (x_ring2_top_TNR1 - width, y_ring2_top_TNR1 - width))
    path22.segment(TNR_tail, '+x', **ld_TNR)
    
    path23 = gdspy.Path(width_TNR, (x_ring2_top_TNR2 + width, y_ring2_top_TNR2 - width))
    path23.segment(TNR_tail, '-x', **ld_TNR)
    
    #######################################################################
    # Metalic pads
    if idx == 0:
        x_rect1 = x_ring1_bottom + 4*bend_radius
    
    y_rect1 = y_ring1_bottom + 0*ring_radius
    offset = (side_M2 - side_silox)/2
    
    for pad_col_idx in range(6):
        pad_shift = pad_col_idx * pad_shift_const
        rect1 = gdspy.Rectangle((x_rect1 + pad_shift         , y_rect1         ), (x_rect1 + pad_shift + side_M2            , y_rect1 + side_M2            ), **ld_METAL2)
        rect2 = gdspy.Rectangle((x_rect1 + pad_shift + offset, y_rect1 + offset), (x_rect1 + pad_shift + offset + side_silox, y_rect1 + offset + side_silox), **ld_Silox)
        
        cell.add(rect1)
        cell.add(rect2)
    
    #######################################################################
    # Metals 1 + 2 lines + Vias
    
    # Vias parameters
    via1_type    = "Contact"
    rows1        = 4
    columns1     = 4
    via1_side    = 0.26
    via1_spacing = 0.26
    side_gap1    = 0.5
    
    via2_type    = "VIA1"
    rows2        = 4
    columns2     = 4
    via2_side    = 0.5
    via2_spacing = 0.5
    side_gap2    = 0.5
    
    via1_width  = round(columns1*via1_side + (columns1 - 1)*via1_spacing + 2*side_gap1, 3)
    via1_height = round(rows1   *via1_side + (rows1 - 1)   *via1_spacing + 2*side_gap1, 3)
    via2_width  = round(columns2*via2_side + (columns2 - 1)*via2_spacing + 2*side_gap2, 3)
    via2_height = round(rows2   *via2_side + (rows2 - 1)   *via2_spacing + 2*side_gap2, 3)
    # via_array(cell, via_type, via_locX, via_locY, rows, columns, via_side, via_spacing, side_gap)
    
    
    
    # # Ring 1 bottom
    path24 = gdspy.Path(width_M1, (x_ring1_bottom_TNR1 - width_M1/2 - width_TNR/2 + TNR_tail, y_ring1_bottom_TNR1 + width_TNR))
    path24.segment(160, '-y', **ld_METAL1)
    via_array(cell, via1_type, x_ring1_bottom_TNR1 - width_M1/2 - width_TNR/2 + TNR_tail - via1_width/2, y_ring1_bottom_TNR1 + width_TNR - via1_height, rows1, columns1, via1_side, via1_spacing, side_gap1)
    path25 = gdspy.Path(width_M2, (path24.x - width_M1/2, path24.y + width_M2/2))
    path25.segment(x_rect1 - path24.x + 1*pad_shift_const + 0.5*side_M2 - width_M2/2 + width_M1/2, '+x', **ld_METAL2)
    path25.turn(width_M2/2, 'l', **ld_METAL2)
    path25.segment(100, **ld_METAL2)
    via_array(cell, via2_type, path24.x - width_M1/2, path24.y + width_M2/2 - via2_height/2, rows2, columns2, via2_side, via2_spacing, side_gap2)
    
    path26 = gdspy.Path(width_M1, (x_ring1_bottom_TNR2 + width_M1/2 + width - TNR_tail, y_ring1_bottom_TNR2))
    path26.segment(y_rect1 + side_M2 + 120 - y_ring1_bottom_TNR2, '+y', **ld_METAL1)
    via_array(cell, via1_type, x_ring1_bottom_TNR2 + width_M1/2 + width_TNR/2 - TNR_tail - via1_width/2, y_ring1_bottom_TNR2, rows1, columns1, via1_side, via1_spacing, side_gap1)
    path27 = gdspy.Path(width_M2, (path26.x - width_M1/2, path26.y - width_M2/2))
    path27.segment(x_rect1 - path26.x + 0*pad_shift_const + 0.5*side_M2 - width_M2/2, '+x', **ld_METAL2)
    path27.turn(width_M2/2, 'r', **ld_METAL2)
    path27.segment(120, **ld_METAL2)
    via_array(cell, via2_type, path26.x - width_M1/2, path26.y - width_M2/2 - via2_height/2, rows2, columns2, via2_side, via2_spacing, side_gap2)
    
    # # Ring 2 bottom
    path28 = gdspy.Path(width_M1, (x_ring2_bottom_TNR1 - width_M1/2 - width_TNR/2 + TNR_tail, y_ring2_bottom_TNR1 + width_TNR))
    path28.segment(270, '-y', **ld_METAL1)
    via_array(cell, via1_type, x_ring2_bottom_TNR1 - width_M1/2 - width_TNR/2 + TNR_tail - via1_width/2, y_ring2_bottom_TNR1 + width_TNR - via1_height, rows1, columns1, via1_side, via1_spacing, side_gap1)
    path29 = gdspy.Path(width_M2, (path28.x + width_M1/2, path28.y + width_M2/2))
    path29.segment(-(x_rect1 - path28.x + 3*pad_shift_const + 0.5*side_M2 + width_M2/2 - width_M1/2), '-x', **ld_METAL2)
    path29.turn(width_M2/2, 'r', **ld_METAL2)
    path29.segment(210, **ld_METAL2)
    via_array(cell, via2_type, path28.x - width_M1/2, path28.y + width_M2/2 - via2_height/2, rows2, columns2, via2_side, via2_spacing, side_gap2)
    
    path30 = gdspy.Path(width_M1, (x_ring2_bottom_TNR2 + width_M1/2 + width - TNR_tail, y_ring2_bottom_TNR2))
    path30.segment(y_rect1 + side_M2 + 120 - y_ring2_bottom_TNR2, '+y', **ld_METAL1)
    via_array(cell, via1_type, x_ring2_bottom_TNR2 + width_M1/2 + width_TNR/2 - TNR_tail - via1_width/2, y_ring2_bottom_TNR2, rows1, columns1, via1_side, via1_spacing, side_gap1)
    path31 = gdspy.Path(width_M2, (path30.x + width_M1/2, path30.y - width_M2/2))
    path31.segment(-(x_rect1 - path30.x + 0*pad_shift_const + 0.5*side_M2 - width_M2/2), '-x', **ld_METAL2)
    via_array(cell, via2_type, path30.x - width_M1/2, path30.y - width_M2/2 - via2_height/2, rows2, columns2, via2_side, via2_spacing, side_gap2)
    
    # # Ring 1 top
    path32 = gdspy.Path(width_M1, (x_ring1_top_TNR1 - width_M1/2 - width + TNR_tail, y_ring1_top_TNR1))
    path32.segment(100, '-y', **ld_METAL1)
    via_array(cell, via1_type, x_ring1_top_TNR1 - width_M1/2 - width_TNR/2 + TNR_tail - via1_width/2, y_ring1_top_TNR1 - via1_height, rows1, columns1, via1_side, via1_spacing, side_gap1)
    path33 = gdspy.Path(width_M2, (path32.x - width_M1/2, path32.y + width_M2/2))
    path33.segment(x_rect1 - path32.x + 2*pad_shift_const + 0.5*side_M2 - width_M2/2 + width_M1/2, '+x', **ld_METAL2)
    path33.turn(width_M2/2, 'l', **ld_METAL2)
    path33.segment(150, **ld_METAL2)
    via_array(cell, via2_type, path32.x - width_M1/2, path32.y + width_M2/2 - via2_height/2, rows2, columns2, via2_side, via2_spacing, side_gap2)
    
    path34 = gdspy.Path(width_M1, (x_ring1_top_TNR2 + width_M1/2 + width - TNR_tail, y_ring1_top_TNR2 - width_TNR))
    path34.segment(y_rect1 + side_M2 + 120 - y_ring1_top_TNR2 + width_TNR, '+y', **ld_METAL1)
    via_array(cell, via1_type, x_ring1_top_TNR2 + width_M1/2 + width_TNR/2 - TNR_tail - via1_width/2, y_ring1_top_TNR2 - width_TNR, rows1, columns1, via1_side, via1_spacing, side_gap1)
    path35 = gdspy.Path(width_M2, (path34.x - width_M1/2, path34.y - width_M2/2))
    path35.segment(x_rect1 - path34.x + 0*pad_shift_const + 0.5*side_M2, '+x', **ld_METAL2)
    via_array(cell, via2_type, path34.x - width_M1/2, path34.y - width_M2/2 - via2_height/2, rows2, columns2, via2_side, via2_spacing, side_gap2)
    
    # # Ring 2 top
    path36 = gdspy.Path(width_M1, (x_ring2_top_TNR1 - width_M1/2 - width + TNR_tail, y_ring2_top_TNR1))
    path36.segment(80, '-y', **ld_METAL1)
    via_array(cell, via1_type, x_ring2_top_TNR1 - width_M1/2 - width_TNR/2 + TNR_tail - via1_width/2, y_ring2_top_TNR1 - via1_height, rows1, columns1, via1_side, via1_spacing, side_gap1)
    path37 = gdspy.Path(width_M2, (path36.x + width_M1/2, path36.y + width_M2/2))
    path37.segment(-(x_rect1 - path36.x + 4*pad_shift_const + 0.5*side_M2 + width_M2/2 - width_M1/2), '-x', **ld_METAL2)
    path37.turn(width_M2/2, 'r', **ld_METAL2)
    path37.segment(130, **ld_METAL2)
    via_array(cell, via2_type, path36.x - width_M1/2, path36.y + width_M2/2 - via2_height/2, rows2, columns2, via2_side, via2_spacing, side_gap2)
    
    path38 = gdspy.Path(width_M1, (x_ring2_top_TNR2 + width_M1/2 + width - TNR_tail, y_ring2_top_TNR2 - width_TNR))
    path38.segment(y_rect1 + side_M2 + 120 - y_ring2_top_TNR2 + width_TNR, '+y', **ld_METAL1)
    via_array(cell, via1_type, x_ring2_top_TNR2 + width_M1/2 + width_TNR/2 - TNR_tail - via1_width/2, y_ring2_top_TNR2 - width_TNR, rows1, columns1, via1_side, via1_spacing, side_gap1)
    path39 = gdspy.Path(width_M2, (path38.x + width_M1/2, path38.y - width_M2/2))
    path39.segment(-(x_rect1 - path38.x + 0*pad_shift_const + 0.5*side_M2 - width_M2/2), '-x', **ld_METAL2)
    via_array(cell, via2_type, path38.x - width_M1/2, path38.y - width_M2/2 - via2_height/2, rows2, columns2, via2_side, via2_spacing, side_gap2)
    
    #######################################################################
    # Create TNR cover on MZI arm
    TNR_path_MZI = gdspy.Path(width_TNR, (MZI_TNR_cover_x - TNR_tail, MZI_TNR_cover_y))
    TNR_path_MZI.segment(TNR_tail - width_TNR/2, '+x', **ld_TNR)
    TNR_path_MZI.turn(width_TNR/2, 'l', **ld_TNR)
    TNR_path_MZI.segment(vertical_out_coup, '+y', **ld_TNR)
    TNR_path_MZI.turn(width_TNR/2, 'r', **ld_TNR)
    TNR_path_MZI.segment(TNR_tail - width_TNR/2, '+x', **ld_TNR)
    MZI_TNR_cover_end_x = TNR_path_MZI.x
    MZI_TNR_cover_end_y = TNR_path_MZI.y
    
    M1_path_MZI1 = gdspy.Path(width_M1, (MZI_TNR_cover_x - TNR_tail + width_M1/2, MZI_TNR_cover_y - width_TNR/2))
    M1_path_MZI1.segment(-(MZI_TNR_cover_y - y_rect1 - side_M2/2 - width_M2/2), '+y', **ld_METAL1)
    via_array(cell, via1_type, MZI_TNR_cover_x - TNR_tail + width_M1/2 - via1_width/2, MZI_TNR_cover_y - width_TNR/2, rows1, columns1, via1_side, via1_spacing, side_gap1)
    M2_path_MZI1 = gdspy.Path(width_M2, (M1_path_MZI1.x + width_M1/2, M1_path_MZI1.y - width_M2/2))
    M2_path_MZI1.segment(-(x_rect1 - M1_path_MZI1.x + 5*pad_shift_const + 0.5*side_M2), '-x', **ld_METAL2)
    via_array(cell, via2_type, M1_path_MZI1.x + width_M1/2 - via2_width, M1_path_MZI1.y - width_M2/2, rows2, columns2, via2_side, via2_spacing, side_gap2)
    
    M1_path_MZI2 = gdspy.Path(width_M1, (MZI_TNR_cover_end_x - width_M1/2, MZI_TNR_cover_end_y - width_TNR/2))
    M1_path_MZI2.segment(y_rect1 + side_M2 + 120 - MZI_TNR_cover_end_y + width_TNR/2, '+y', **ld_METAL1)
    via_array(cell, via1_type, MZI_TNR_cover_end_x - width_M1/2 - via1_width/2, MZI_TNR_cover_end_y - width_TNR/2, rows1, columns1, via1_side, via1_spacing, side_gap1)
    M2_path_MZI2 = gdspy.Path(width_M2, (M1_path_MZI2.x + width_M1/2, M1_path_MZI2.y - width_M2/2))
    M2_path_MZI2.segment(-(x_rect1 - M1_path_MZI2.x + 5*pad_shift_const + 0.5*side_M2), '-x', **ld_METAL2)
    via_array(cell, via2_type, M1_path_MZI2.x + width_M1/2 - via2_width, M1_path_MZI2.y - width_M2/2, rows2, columns2, via2_side, via2_spacing, side_gap2)
    
    #######################################################################
    # Add all paths
    cell.add(path1)
    cell.add(path2)
    cell.add(path3)
    cell.add(path4)
    cell.add(path5)
    cell.add(path6)
    cell.add(path7)
    cell.add(path8)
    cell.add(path9)
    cell.add(path10)
    cell.add(path11)
    cell.add(path12)
    cell.add(path13)
    cell.add(path14)
    cell.add(path15)
    cell.add(path16)
    cell.add(path17)
    cell.add(path18)
    cell.add(path19)
    cell.add(path20)
    cell.add(path21)
    cell.add(path22)
    cell.add(path23)
    cell.add(path24)
    cell.add(path25)
    cell.add(path26)
    cell.add(path27)
    cell.add(path28)
    cell.add(path29)
    cell.add(path30)
    cell.add(path31)
    cell.add(path32)
    cell.add(path33)
    cell.add(path34)
    cell.add(path35)
    cell.add(path36)
    cell.add(path37)
    cell.add(path38)
    cell.add(path39)
    cell.add(TNR_path_MZI)
    cell.add(M1_path_MZI1)
    cell.add(M2_path_MZI1)
    cell.add(M1_path_MZI2)
    cell.add(M2_path_MZI2)
    cell.add(start_taper)

gdspy.LayoutViewer(lib)
if overwrite == 1:
    lib.write_gds("elliptical2.gds")

gdspy.current_library = gdspy.GdsLibrary()




#/data/tower/ph18/HOTCODE/amslibs/cds_oa/cdslibs/ph18/devices/devices_ph18mx/ph18.layermap