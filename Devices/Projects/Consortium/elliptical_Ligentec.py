# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Units: um

import numpy
import gdspy
from via_array_Ligentec import via_array_Ligentec
from s_bend_func import sbendPath, sbendPathM

overwrite = 1 # 1 - Overwrite GDS, 0 - Don't overwrite
lib = gdspy.GdsLibrary()
cell = lib.new_cell('Elliptical_Filter')


# Layers:
ld_NWG          = {"layer": 2,      "datatype": 0}
ld_Silox        = {"layer": 33,     "datatype": 0}
ld_HTR          = {"layer": 30,     "datatype": 0}
ld_Contact      = {"layer": 31,      "datatype": 0}
ld_METAL1       = {"layer": 32,      "datatype": 0}

# Parameters:
width               = 1
width_HTR           = 2*width
width_HTR_ext       = 3.52
width_M1            = 20*width
taper_len           = 200
final_taper_width   = 0.3    
bend_radius         = 80
ring_radius         = 100
fiber_gap           = 127
safety_gap          = 30
coup_gap            = 0.3
run_x_start         = 2*bend_radius + safety_gap
vertical_50_coup    = safety_gap/2 + ring_radius - bend_radius
vertical_out_coup   = 2 * bend_radius + coup_gap
Lc_50_coup          = 10
Lc_test_port        = 0
side_pad            = 100
side_silox          = 80
pad_shift_const     = 125
HTR_tail            = 30
L_sbend              = 200
# Lc_D3_vec           = [4.95, 14.15, 10.75, 19.95]
# Lc_D4_vec           = [9.65, 18.85, 6.81, 15.9]
# Lc_D3_vec           = [4.95,  6,  7,  8,  9, 10, 11, 12, 14.15]
# Lc_D4_vec           = [9.65, 11, 12, 13, 14, 15, 16, 17, 18.85]
Lc_D3_vec           = [4.95,  6.5,  7.5,  9.0, 10.0, 11.5, 12.5, 14.15]
Lc_D4_vec           = [9.65, 11.0, 12.5, 13.5, 15.0, 16.0, 17.5, 18.85]
run_x_through_coup  = 7 * bend_radius + Lc_test_port
right_end           = 5000 - taper_len - 10 - 10
numPads             = 16


for idx in range(len(Lc_D3_vec)):
    # Sweep parameters
    Lc_D3 = Lc_D3_vec[idx]
    Lc_D4 = Lc_D4_vec[idx]
    run_x_through_ring1 = 3 * bend_radius + Lc_D3
    run_x_through_ring2 = 3 * bend_radius + Lc_D4
    
    
    #######################################################################
    # Start path1 (bottom track)
    path1 = gdspy.Path(width, (taper_len, -idx * 4*fiber_gap))
    x_start = path1.x
    y_start = path1.y
    sbendPathM(path1,run_x_start, fiber_gap - safety_gap)
    # path1.segment(run_x_start, "+x", **ld_NWG)
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
    path1.segment(Lc_test_port, **ld_NWG)
    x_out_coup_bottom = path1.x
    y_out_coup_bottom = path1.y
    path1.turn(bend_radius, "l", **ld_NWG)
    path1.turn(bend_radius, "rr", **ld_NWG)
    path1.segment(vertical_out_coup, **ld_NWG)
    MZI_HTR_cover_x = path1.x
    MZI_HTR_cover_y = path1.y
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
    # Turn to create S shape
    path1.turn(bend_radius, "ll", **ld_NWG)
    path1.turn(bend_radius, "r", **ld_NWG)
    sbendPath(path1, 2*bend_radius + vertical_50_coup - 2*fiber_gap + safety_gap + coup_gap + width + L_sbend, 2*bend_radius + vertical_50_coup - 2*fiber_gap + safety_gap + coup_gap + width)
    # Continue a bit to align all
    path1.segment(right_end - path1.x, **ld_NWG)
    # Add tapers at both ends
    path1.segment(taper_len, final_width=final_taper_width, **ld_NWG)
    start_taper = gdspy.Path(width, (x_start, y_start))
    start_taper.segment(taper_len, "-x", final_width=final_taper_width, **ld_NWG)
    
    #######################################################################
    # Start path2 + path3 (bottom WG couples to bottom track)
    path3 = gdspy.Path(width, (x_out_coup_bottom, y_out_coup_bottom - coup_gap - width))
    path3.segment(Lc_test_port, "-x", **ld_NWG)
    path3.turn(bend_radius, "l", **ld_NWG)
    path3.segment(safety_gap - width, **ld_NWG)
    path3.turn(bend_radius, "r", **ld_NWG)
    path3.segment(20*bend_radius + 2*Lc_D3 + Lc_50_coup + Lc_test_port + run_x_start, **ld_NWG)
    path3.segment(taper_len, final_width=final_taper_width, **ld_NWG)
    y_bottom = path3.y
    
    path2 = gdspy.Path(width, (x_out_coup_bottom, y_out_coup_bottom - coup_gap - width))
    path2.turn(bend_radius, "r", **ld_NWG)
    path2.segment(safety_gap - width, **ld_NWG)
    path2.turn(bend_radius, "l", **ld_NWG)
    path2.segment(13*bend_radius + 2*Lc_D4 + Lc_50_coup + safety_gap+100, **ld_NWG)
    # sbend to create gap for fiber array (127um)
    sbendPath(path2, L_sbend, 4*bend_radius + 2*vertical_50_coup - 3*fiber_gap + 2*safety_gap + coup_gap + width)
    # Continue a bit to align all
    path2.segment(right_end - path2.x, **ld_NWG)
    # Add taper
    path2.segment(taper_len, final_width=final_taper_width, **ld_NWG)
    
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
    path4.segment(Lc_test_port, **ld_NWG)
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
    # Turn to create S shape
    path4.turn(bend_radius, "l", **ld_NWG)
    path34 = gdspy.Path(width, (start_taper.x + taper_len, start_taper.y + fiber_gap))
    sbendPath(path34, L_sbend, path4.y - (y_start + fiber_gap))
    # Add taper
    path35 = gdspy.Path(width, (start_taper.x + taper_len, start_taper.y + fiber_gap))
    path35.segment(-taper_len, final_width=final_taper_width, **ld_NWG)
    
    # Complete right part of the "bump" for the right 50 coupler
    path5 = gdspy.Path(width, (x_50_coup2_bottom, y_50_coup2_bottom + coup_gap + width))
    # Complete right part of the "bump"
    path5.turn(bend_radius, "l", **ld_NWG)
    path5.segment(vertical_50_coup, **ld_NWG)
    path5.turn(bend_radius, "r", **ld_NWG)
    # sbend to create gap for fiber array (127um)
    sbendPathM(path5, fiber_gap - safety_gap + L_sbend, fiber_gap - safety_gap)
    # Continue a bit to align all
    path5.segment(right_end - path5.x, **ld_NWG)
    # Add taper
    path5.segment(taper_len, final_width=final_taper_width, **ld_NWG)
    
    
    #######################################################################
    # Start path6 + path7 (top WG couples to top track)
    path6 = gdspy.Path(width, (x_out_coup_top, y_out_coup_top + coup_gap + width))
    path6.segment(Lc_test_port, "-x", **ld_NWG)
    path6.turn(bend_radius, "r", **ld_NWG)
    path6.segment(safety_gap - width, **ld_NWG)
    path6.turn(bend_radius, "l", **ld_NWG)
    # path6.segment(13*bend_radius + Lc_D3 + Lc_D4 + Lc_50_coup + safety_gap, **ld_NWG)
    path6.segment(path6.x - (taper_len + L_sbend), **ld_NWG)
    path32 = gdspy.Path(width, (path35.x + taper_len, path35.y + fiber_gap))
    sbendPath(path32, L_sbend, path6.y - (y_start + 2*fiber_gap))
    # Add taper
    path33 = gdspy.Path(width, (path35.x + taper_len, path35.y + fiber_gap))
    path33.segment(-taper_len, final_width=final_taper_width, **ld_NWG)
    
    path7 = gdspy.Path(width, (x_out_coup_top, y_out_coup_top + coup_gap + width))
    path7.turn(bend_radius, "l", **ld_NWG)
    path7.segment(safety_gap - width, **ld_NWG)
    path7.turn(bend_radius, "r", **ld_NWG)
    path7.segment(20*bend_radius + Lc_D3 + Lc_D4 + Lc_50_coup + Lc_test_port, **ld_NWG)
    # Continue a bit to align all
    path7.segment(right_end - path7.x, **ld_NWG)
    # Add taper
    path7.segment(taper_len, final_width=final_taper_width, **ld_NWG)
    y_top = path7.y
    
    
    #######################################################################
    # Start path8+path12 (ring1 bottom) - NWG + HTR cover
    path8 = gdspy.Path(width, (x_ring1_bottom, y_ring1_bottom + coup_gap + width))
    path8.turn(ring_radius, "ll", **ld_NWG)
    path8.segment(Lc_D3, **ld_NWG)
    path8.turn(ring_radius, "ll", **ld_NWG)
    path8.segment(Lc_D3, **ld_NWG)
    
    path12 = gdspy.Path(width_HTR, (x_ring1_bottom + ring_radius, y_ring1_bottom + ring_radius + coup_gap + width))
    path12.segment(0, '+y', **ld_HTR)
    x_ring1_bottom_HTR1 = path12.x
    y_ring1_bottom_HTR1 = path12.y
    path12.turn(ring_radius, "l", **ld_HTR)
    path12.segment(Lc_D3, **ld_HTR)
    path12.turn(ring_radius, "l", **ld_HTR)
    x_ring1_bottom_HTR2 = path12.x
    y_ring1_bottom_HTR2 = path12.y
    
    #######################################################################
    # Start path9+path13 (ring2 bottom) - NWG + HTR cover
    path9 = gdspy.Path(width, (x_ring2_bottom, y_ring2_bottom + coup_gap + width))
    path9.turn(ring_radius, "ll", **ld_NWG)
    path9.segment(Lc_D4, **ld_NWG)
    path9.turn(ring_radius, "ll", **ld_NWG)
    path9.segment(Lc_D4, **ld_NWG)
    
    path13 = gdspy.Path(width_HTR, (x_ring2_bottom + ring_radius, y_ring2_bottom + ring_radius + coup_gap + width))
    path13.segment(0, '+y', **ld_HTR)
    x_ring2_bottom_HTR1 = path13.x
    y_ring2_bottom_HTR1 = path13.y
    path13.turn(ring_radius, "l", **ld_HTR)
    path13.segment(Lc_D4, **ld_HTR)
    path13.turn(ring_radius, "l", **ld_HTR)
    x_ring2_bottom_HTR2 = path13.x
    y_ring2_bottom_HTR2 = path13.y
    
    #######################################################################
    # Start path10+path14 (ring1 top) - NWG + HTR cover
    path10 = gdspy.Path(width, (x_ring1_top, y_ring1_top - coup_gap - width))
    path10.turn(ring_radius, "rr", **ld_NWG)
    path10.segment(Lc_D3, **ld_NWG)
    path10.turn(ring_radius, "rr", **ld_NWG)
    path10.segment(Lc_D3, **ld_NWG)
    
    path14 = gdspy.Path(width_HTR, (x_ring1_top + ring_radius, y_ring1_top - ring_radius - coup_gap - width))
    path14.segment(0, '-y', **ld_HTR)
    x_ring1_top_HTR1 = path14.x
    y_ring1_top_HTR1 = path14.y
    path14.turn(ring_radius, "r", **ld_HTR)
    path14.segment(Lc_D3, **ld_HTR)
    path14.turn(ring_radius, "r", **ld_HTR)
    x_ring1_top_HTR2 = path14.x
    y_ring1_top_HTR2 = path14.y
    
    #######################################################################
    # Start path11+path15 (ring2 top) - NWG + HTR cover
    path11 = gdspy.Path(width, (x_ring2_top, y_ring2_top - coup_gap - width))
    path11.turn(ring_radius, "rr", **ld_NWG)
    path11.segment(Lc_D4, **ld_NWG)
    path11.turn(ring_radius, "rr", **ld_NWG)
    path11.segment(Lc_D4, **ld_NWG)
    
    path15 = gdspy.Path(width_HTR, (x_ring2_top + ring_radius, y_ring2_top - ring_radius - coup_gap - width))
    path15.segment(0, '-y', **ld_HTR)
    x_ring2_top_HTR1 = path15.x
    y_ring2_top_HTR1 = path15.y
    path15.turn(ring_radius, "r", **ld_HTR)
    path15.segment(Lc_D4, **ld_HTR)
    path15.turn(ring_radius, "r", **ld_HTR)
    x_ring2_top_HTR2 = path15.x
    y_ring2_top_HTR2 = path15.y

    #######################################################################
    # Metalic pads
    if idx == 0:
        x_rect1 = x_ring1_bottom + 4*bend_radius - 600
    
    y_rect1 = y_ring1_bottom + 0*ring_radius + 160
    offset = (side_pad - side_silox)/2
    
    pad_locs_X = []
    
    for pad_col_idx in range(numPads):
        pad_shift = pad_col_idx * pad_shift_const
        rect1 = gdspy.Rectangle((x_rect1 + pad_shift         , y_rect1         ), (x_rect1 + pad_shift + side_pad           , y_rect1 + side_pad           ), **ld_METAL1)
        rect2 = gdspy.Rectangle((x_rect1 + pad_shift + offset, y_rect1 + offset), (x_rect1 + pad_shift + offset + side_silox, y_rect1 + offset + side_silox), **ld_Silox)
        
        pad_locs_X += [x_rect1 + pad_shift]
        
        cell.add(rect1)
        cell.add(rect2)

    #######################################################################
    # HTR extensions from rings
    path16 = gdspy.Path(width_HTR_ext, (x_ring1_bottom_HTR1 - width, y_ring1_bottom_HTR1 + width_HTR_ext/2))
    path16.segment(HTR_tail, '+x', **ld_HTR)
    
    path17 = gdspy.Path(width_HTR_ext, (x_ring1_bottom_HTR2 + width, y_ring1_bottom_HTR2 + width_HTR_ext/2))
    path17.segment(HTR_tail, '-x', **ld_HTR)
    
    path18 = gdspy.Path(width_HTR_ext, (x_ring2_bottom_HTR1 - width, y_ring2_bottom_HTR1 + width_HTR_ext/2))
    path18.segment(HTR_tail, '+x', **ld_HTR)
    
    path19 = gdspy.Path(width_HTR_ext, (x_ring2_bottom_HTR2 + width, y_ring2_bottom_HTR2 + width_HTR_ext/2))
    path19.segment(HTR_tail, '-x', **ld_HTR)
    
    path20 = gdspy.Path(width_HTR_ext, (x_ring1_top_HTR1 - width, y_ring1_top_HTR1 - width_HTR_ext/2))
    path20.segment(x_ring1_bottom_HTR2 - x_ring1_top_HTR1 - HTR_tail + width_M1 + width_HTR, '+x', **ld_HTR)
    
    path21 = gdspy.Path(width_HTR_ext, (x_ring1_top_HTR2 + width, y_ring1_top_HTR2 - width_HTR_ext/2))
    path21.segment(HTR_tail, '-x', **ld_HTR)
    
    path22 = gdspy.Path(width_HTR_ext, (x_ring2_top_HTR1 - width, y_ring2_top_HTR1 - width_HTR_ext/2))
    path22.segment(x_ring2_bottom_HTR2 - x_ring2_top_HTR1 - HTR_tail + width_M1 + width_HTR, '+x', **ld_HTR)
    
    path23 = gdspy.Path(width_HTR_ext, (x_ring2_top_HTR2 + width, y_ring2_top_HTR2 - width_HTR_ext/2))
    path23.segment(x_ring2_top_HTR2 + width_M1/2 - (pad_locs_X[13] + side_pad/2), '-x', **ld_HTR)
    
    #######################################################################
    # Metals 1 + 2 lines + Vias
    
    # Vias parameters
    via1_type    = "Contact"
    rows1        = 4
    columns1     = 25
    via1_side    = 0.36
    via1_spacing = 0.36
    side_gap1    = 0.5
    
    via1_width  = round(columns1*via1_side + (columns1 - 1)*via1_spacing + 2*side_gap1, 3)
    via1_height = round(rows1   *via1_side + (rows1 - 1)   *via1_spacing + 2*side_gap1, 3)
    # via_array_Ligentec(cell, via_type, via_locX, via_locY, rows, columns, via_side, via_spacing, side_gap)
    
    
    # # Ring 1 bottom
    path24 = gdspy.Path(width_M1, (x_ring1_bottom_HTR1 - width_M1/2 - width_HTR/2 + HTR_tail, y_ring1_bottom_HTR1 + width_HTR_ext))
    path24.segment(60, '-y', **ld_METAL1)
    path24.turn(width_M1/2, 'r', **ld_METAL1)
    path24.segment(-(pad_locs_X[2] + side_pad/2 - (x_ring1_bottom_HTR1 + width_M1/2 + width - HTR_tail) - width_M1), '-x', **ld_METAL1)
    path24.turn(width_M1/2, 'r', **ld_METAL1)
    path24.segment(y_rect1 + side_pad/2 - y_ring1_bottom_HTR1 + 60, '+y', **ld_METAL1)
    via_array_Ligentec(cell, via1_type, x_ring1_bottom_HTR1 - width_M1/2 - width_HTR/2 + HTR_tail - via1_width/2, y_ring1_bottom_HTR1 + width_HTR_ext - via1_height, rows1, columns1, via1_side, via1_spacing, side_gap1)
    
    #path25 = gdspy.Path(width_M1, (x_ring1_bottom_HTR2 + width_M1/2 + width - HTR_tail, y_ring1_bottom_HTR2))
    #path25.segment(y_rect1 + side_pad/2 - y_ring1_bottom_HTR2, '+y', **ld_METAL1)
    via_array_Ligentec(cell, via1_type, x_ring1_bottom_HTR2 + width_M1/2 + width_HTR/2 - HTR_tail - via1_width/2, y_ring1_bottom_HTR2, rows1, columns1, via1_side, via1_spacing, side_gap1)
    
    # # Ring 2 bottom
    path26 = gdspy.Path(width_M1, (x_ring2_bottom_HTR1 - width_M1/2 - width_HTR/2 + HTR_tail, y_ring2_bottom_HTR1))
    path26.segment(y_rect1 + side_pad/2 - y_ring2_bottom_HTR1 - width_M1 + 2*width_HTR_ext, '+y', **ld_METAL1)
    path26.turn(width_M1/2, 'l', **ld_METAL1)
    path26.segment(-(pad_locs_X[15] + side_pad/2 - (x_ring2_bottom_HTR1 + width_M1/2 + width - HTR_tail)), '-x', **ld_METAL1)
    via_array_Ligentec(cell, via1_type, x_ring2_bottom_HTR1 - width_M1/2 - width_HTR/2 + HTR_tail - via1_width/2, y_ring2_bottom_HTR1 + width_HTR_ext - via1_height, rows1, columns1, via1_side, via1_spacing, side_gap1)
    
    path27 = gdspy.Path(width_M1, (x_ring2_bottom_HTR2 + width_M1/2 + width - HTR_tail, y_ring2_bottom_HTR2 + width_HTR_ext))
    path27.segment(70, '-y', **ld_METAL1)
    path27.turn(width_M1/2, 'r', **ld_METAL1)
    path27.segment(-(pad_locs_X[14] + side_pad/2 - (x_ring2_bottom_HTR2 + width_M1/2 + width - HTR_tail) + width_M1), '-x', **ld_METAL1)
    path27.turn(width_M1/2, 'r', **ld_METAL1)
    path27.segment(y_rect1 + side_pad/2 - y_ring2_bottom_HTR2 + 70, '+y', **ld_METAL1)
    via_array_Ligentec(cell, via1_type, x_ring2_bottom_HTR2 + width_M1/2 + width_HTR/2 - HTR_tail - via1_width/2, y_ring2_bottom_HTR2, rows1, columns1, via1_side, via1_spacing, side_gap1)
    
    # # Ring 1 top
    path28 = gdspy.Path(width_M1, (x_ring1_bottom_HTR2 + width_M1/2 + width - HTR_tail, y_ring1_top_HTR1 - width_HTR_ext))
    path28.segment(y_rect1 + side_pad/2 - y_ring1_top_HTR1, '+y', **ld_METAL1)
    #path28.segment(2, '+x', **ld_METAL1)
    #path28.segment((y_ring1_bottom_HTR2 + width_HTR_ext) - (y_ring1_top_HTR1 - width_HTR_ext) - 70, '+y', **ld_METAL1)
    via_array_Ligentec(cell, via1_type, x_ring1_bottom_HTR2 + width_M1/2 + width_HTR/2 - HTR_tail - via1_width/2, y_ring1_top_HTR1 - via1_height, rows1, columns1, via1_side, via1_spacing, side_gap1)
    
    path29 = gdspy.Path(width_M1, (x_ring1_top_HTR2 + width_M1/2 + width - HTR_tail, y_ring1_top_HTR2 - width_HTR_ext))
    path29.segment(y_rect1 + side_pad/2 - y_ring1_top_HTR2 - 140, '+y', **ld_METAL1)
    path29.turn(width_M1/2, 'r', **ld_METAL1)
    path29.segment(pad_locs_X[0] + side_pad/2 - (x_ring1_top_HTR2 + width_M1/2 + width - HTR_tail) - width_M1, '+x', **ld_METAL1)
    path29.turn(width_M1/2, 'l', **ld_METAL1)
    path29.segment(140, '+y', **ld_METAL1)
    via_array_Ligentec(cell, via1_type, x_ring1_top_HTR2 + width_M1/2 + width_HTR/2 - HTR_tail - via1_width/2, y_ring1_top_HTR2 - width_HTR_ext, rows1, columns1, via1_side, via1_spacing, side_gap1)
    
    # # Ring 2 top
    path30 = gdspy.Path(width_M1, (x_ring2_bottom_HTR2 + width_M1/2 + width - HTR_tail, y_ring2_top_HTR1 - width_HTR_ext))
    path30.segment(70, '+y', **ld_METAL1)
    via_array_Ligentec(cell, via1_type, x_ring2_bottom_HTR2 + width_M1/2 + width_HTR/2 - HTR_tail - via1_width/2, y_ring2_top_HTR1 - via1_height, rows1, columns1, via1_side, via1_spacing, side_gap1)
    
    path31 = gdspy.Path(width_M1, (pad_locs_X[13] + side_pad/2 + width_HTR/2, y_ring2_top_HTR2 - width_HTR_ext))
    path31.segment(y_rect1 + side_pad/2 - y_ring2_top_HTR2, '+y', **ld_METAL1)
    via_array_Ligentec(cell, via1_type, pad_locs_X[13] + side_pad/2 + width_HTR/2 - width_M1/2 + width/2 + via1_spacing/2, y_ring2_top_HTR2 - width_HTR_ext, rows1, columns1, via1_side, via1_spacing, side_gap1)
    
    #######################################################################
    # Create HTR cover on MZI arm
    HTR_path_MZI = gdspy.Path(width_HTR, (MZI_HTR_cover_x - HTR_tail, MZI_HTR_cover_y))
    HTR_path_MZI.segment(HTR_tail - width_HTR/2, '+x', **ld_HTR)
    HTR_path_MZI.turn(width_HTR/2, 'l', **ld_HTR)
    HTR_path_MZI.segment(vertical_out_coup, '+y', **ld_HTR)
    HTR_path_MZI.turn(width_HTR/2, 'r', **ld_HTR)
    HTR_path_MZI.segment(HTR_tail - width_HTR/2, '+x', **ld_HTR)
    MZI_HTR_cover_end_x = HTR_path_MZI.x
    MZI_HTR_cover_end_y = HTR_path_MZI.y
    
    M1_path_MZI1 = gdspy.Path(width_M1, (MZI_HTR_cover_x - HTR_tail + width_M1/2, MZI_HTR_cover_y - width_HTR/2))
    M1_path_MZI1.segment(70, '+y', **ld_METAL1)
    M1_path_MZI1.turn(width_M1/2, 'l', **ld_METAL1)
    M1_path_MZI1.segment(-(pad_locs_X[11] + side_pad/2 - (MZI_HTR_cover_x - width_M1/2) + width_M1), '-x', **ld_METAL1)
    M1_path_MZI1.turn(width_M1/2, 'r', **ld_METAL1)
    M1_path_MZI1.segment(y_rect1 + side_pad/2 - MZI_HTR_cover_y - 70, '+y', **ld_METAL1)
    via_array_Ligentec(cell, via1_type, MZI_HTR_cover_x - HTR_tail + width_M1/2 - via1_width/2, MZI_HTR_cover_y - width_HTR/2, rows1, columns1, via1_side, via1_spacing, side_gap1)

    
    M1_path_MZI2 = gdspy.Path(width_M1, (MZI_HTR_cover_end_x - width_M1/2, MZI_HTR_cover_end_y - width_HTR/2))
    M1_path_MZI2.segment(30, '+y', **ld_METAL1)
    M1_path_MZI2.turn(width_M1/2, 'l', **ld_METAL1)
    M1_path_MZI2.segment(-(pad_locs_X[12] + side_pad/2 - (MZI_HTR_cover_end_x - width_M1/2) + width_M1), '-x', **ld_METAL1)
    M1_path_MZI2.turn(width_M1/2, 'r', **ld_METAL1)
    M1_path_MZI2.segment(y_rect1 + side_pad/2 - MZI_HTR_cover_end_y - 30, '+y', **ld_METAL1)
    via_array_Ligentec(cell, via1_type, MZI_HTR_cover_end_x - width_M1/2 - via1_width/2, MZI_HTR_cover_end_y - width_HTR/2, rows1, columns1, via1_side, via1_spacing, side_gap1)
    
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
    #cell.add(path25)
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
    cell.add(HTR_path_MZI)
    cell.add(M1_path_MZI1)
    cell.add(M1_path_MZI2)
    cell.add(start_taper)

gdspy.LayoutViewer(lib)
if overwrite == 1:
    lib.write_gds("elliptical_Ligentec.gds")

gdspy.current_library = gdspy.GdsLibrary()




#/data/tower/ph18/HOTCODE/amslibs/cds_oa/cdslibs/ph18/devices/devices_ph18mx/ph18.layermap