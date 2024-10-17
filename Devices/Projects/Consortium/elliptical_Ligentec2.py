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

overwrite = 0 # 1 - Overwrite GDS, 0 - Don't overwrite
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
taper_len           = 150
final_taper_width   = 0.2    
bend_radius         = 80
ring_radius         = 100
fiber_gap           = 127
safety_gap          = 30
coup_gap            = 0.8
run_x_start         = 2*bend_radius + safety_gap
vertical_50_coup    = safety_gap/2 + ring_radius - bend_radius
vertical_out_coup   = safety_gap - width - coup_gap
Lc_50_coup          = 10
Lc_test_port        = 0
side_pad            = 100
side_silox          = 80
pad_shift_const     = 125
HTR_tail            = 30
L_sbend             = 200
coup_gap_ring12_vec = [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80]
coup_gap_ring34_vec = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]
run_x_through_coup  = 7 * bend_radius + Lc_test_port
right_end           = 4870
numPads             = 16
Yjunc_x             = 180 - 2*5
Yjunc_y             = 24.54
HTR_MZI_len         = 300


for idx in range(len(coup_gap_ring12_vec)):
    # Sweep parameters
    coup_gap_ring12 = coup_gap_ring12_vec[idx]
    coup_gap_ring34 = coup_gap_ring34_vec[idx]
    
    #######################################################################
    # Start path1 (bottom track)
    start_taper1 = gdspy.Path(width, (taper_len, -idx * 3*fiber_gap))
    start_taper1.segment(taper_len, "-x", final_width=final_taper_width, **ld_NWG)
    
    path1 = gdspy.Path(width, (taper_len + Yjunc_x, -idx * 3*fiber_gap - Yjunc_y/2))
    sbendPathM(path1, ring_radius + safety_gap - Yjunc_y/2 + L_sbend, ring_radius + safety_gap - Yjunc_y/2)
    # Run through ring + Couple to ring
    path1.segment(4*ring_radius + safety_gap + 70, **ld_NWG)
    # Double "bump" for coupler
    path1.turn(bend_radius, "l", **ld_NWG)
    path1.turn(bend_radius, "rr", **ld_NWG)
    path1.segment(vertical_out_coup, **ld_NWG)
    path1.turn(bend_radius, "l", **ld_NWG)
    x_out_coup_bottom = path1.x
    y_out_coup_bottom = path1.y
    path1.turn(bend_radius, "l", **ld_NWG)
    path1.segment(vertical_out_coup, **ld_NWG)
    path1.turn(bend_radius, "rr", **ld_NWG)
    path1.turn(bend_radius, "l", **ld_NWG)
    # Run through ring + Couple to ring + run through double bump
    path1.segment(4*ring_radius + safety_gap + 8*bend_radius, **ld_NWG)
    sbendPath(path1, ring_radius + safety_gap - Yjunc_y/2 + L_sbend, ring_radius + safety_gap - Yjunc_y/2)
    
    # Start path2 (top track)
    path2 = gdspy.Path(width, (taper_len + Yjunc_x, -idx * 3*fiber_gap + Yjunc_y/2))
    sbendPath(path2, ring_radius + safety_gap - Yjunc_y/2 + L_sbend, ring_radius + safety_gap - Yjunc_y/2)
    # Run through ring + Couple to ring + run through double bump
    path2.segment(4*ring_radius + safety_gap + 8*bend_radius - 70, **ld_NWG)
    # Double "bump" for coupler
    path2.turn(bend_radius, "r", **ld_NWG)
    path2.turn(bend_radius, "ll", **ld_NWG)
    path2.segment(vertical_out_coup, **ld_NWG)
    path2.turn(bend_radius, "r", **ld_NWG)
    x_out_coup_top = path2.x
    y_out_coup_top = path2.y
    path2.turn(bend_radius, "r", **ld_NWG)
    path2.segment(vertical_out_coup, **ld_NWG)
    path2.turn(bend_radius, "ll", **ld_NWG)
    path2.turn(bend_radius, "r", **ld_NWG)
    # Run through ring + Couple to ring
    path2.segment(4*ring_radius + safety_gap + 70, **ld_NWG)
    sbendPathM(path2, path1.x - path2.x, ring_radius + safety_gap - Yjunc_y/2)
    
    # Start path3 (top WG couples to top track)
    start_taper2 = gdspy.Path(width, (taper_len, -idx * 3*fiber_gap + fiber_gap))
    start_taper2.segment(taper_len, "-x", final_width=final_taper_width, **ld_NWG)
    
    path3 = gdspy.Path(width, (taper_len, -idx * 3*fiber_gap + fiber_gap))
    sbendPath(path3, ring_radius + 2*safety_gap - fiber_gap + L_sbend, ring_radius + 2*safety_gap - fiber_gap)
    path3.segment(right_end - taper_len - (ring_radius + 2*safety_gap - fiber_gap + L_sbend) - path3.x, **ld_NWG)
    sbendPathM(path3, ring_radius + 2*safety_gap - fiber_gap + L_sbend, ring_radius + 2*safety_gap - fiber_gap)
    path3.segment(taper_len, final_width=final_taper_width, **ld_NWG)
    
    # Start path4 (bottom WG couples to bottom track)
    start_taper3 = gdspy.Path(width, (taper_len, -idx * 3*fiber_gap - fiber_gap))
    start_taper3.segment(taper_len, "-x", final_width=final_taper_width, **ld_NWG)
    
    path4 = gdspy.Path(width, (taper_len, -idx * 3*fiber_gap - fiber_gap))
    sbendPathM(path4, ring_radius + 2*safety_gap - fiber_gap + L_sbend, ring_radius + 2*safety_gap - fiber_gap)
    path4.segment(right_end - taper_len - (ring_radius + 2*safety_gap - fiber_gap + L_sbend) - path4.x, **ld_NWG)
    sbendPath(path4, ring_radius + 2*safety_gap - fiber_gap + L_sbend, ring_radius + 2*safety_gap - fiber_gap)
    path4.segment(taper_len, final_width=final_taper_width, **ld_NWG)
    
    # Start path5 (Combined top and bottom tracks)
    path5 = gdspy.Path(width, (path1.x + Yjunc_x, path1.y + Yjunc_y/2))
    path5.segment(right_end - taper_len - path5.x, **ld_NWG)
    path5.segment(taper_len, final_width=final_taper_width, **ld_NWG)
    
    
    # ring 1
    ring1_loc_x = taper_len + Yjunc_x + ring_radius + safety_gap - Yjunc_y/2 + L_sbend + ring_radius - 50
    ring1_loc_y = -idx * 3*fiber_gap + ring_radius + safety_gap - width - coup_gap_ring12
    ring1 = gdspy.Path(width, (ring1_loc_x, ring1_loc_y))
    ring1.turn(ring_radius, "rr", **ld_NWG)
    ring1.turn(ring_radius, "rr", **ld_NWG)
    
    # ring 2
    ring2_loc_x = taper_len + Yjunc_x + ring_radius + 2*safety_gap - Yjunc_y/2 + L_sbend + 3*ring_radius + 40
    ring2_loc_y = -idx * 3*fiber_gap - ring_radius - safety_gap + width + coup_gap_ring12
    ring2 = gdspy.Path(width, (ring2_loc_x, ring2_loc_y))
    ring2.turn(ring_radius, 2*numpy.pi, **ld_NWG)
    
    # ring 3
    ring3_loc_x = taper_len + Yjunc_x + 6*ring_radius + 2*safety_gap - Yjunc_y/2 + L_sbend + 16*bend_radius - 50
    ring3_loc_y = -idx * 3*fiber_gap + ring_radius + safety_gap - width - coup_gap_ring34
    ring3 = gdspy.Path(width, (ring3_loc_x, ring3_loc_y))
    ring3.turn(ring_radius, "rr", **ld_NWG)
    ring3.turn(ring_radius, "rr", **ld_NWG)
    
    # ring 4
    ring4_loc_x = taper_len + Yjunc_x + 8*ring_radius + 3*safety_gap - Yjunc_y/2 + L_sbend + 16*bend_radius + 40
    ring4_loc_y = -idx * 3*fiber_gap - ring_radius - safety_gap + width + coup_gap_ring34
    ring4 = gdspy.Path(width, (ring4_loc_x, ring4_loc_y))
    ring4.turn(ring_radius, 2*numpy.pi, **ld_NWG)
    
    # Heater on MZI arm
    HTR_MZI = gdspy.Path(width_HTR, (x_out_coup_bottom + 4*bend_radius, y_out_coup_bottom + vertical_out_coup))
    HTR_MZI_ext_left = gdspy.Path(width_HTR_ext, (HTR_MZI.x + width_HTR_ext/2, HTR_MZI.y - width_HTR/2))
    HTR_MZI_ext_left.segment(HTR_tail, '+y', **ld_HTR)
    HTR_MZI_ext_left.turn(width_HTR_ext/2, 'r', **ld_HTR)
    HTR_MZI_ext_left.segment(HTR_tail, '+x', **ld_HTR)
    HTR_MZI.segment(HTR_MZI_len, '+x', **ld_HTR)
    HTR_MZI_ext_right = gdspy.Path(width_HTR_ext, (HTR_MZI.x - width_HTR_ext/2, HTR_MZI.y - width_HTR/2))
    HTR_MZI_ext_right.segment(HTR_tail, '+y', **ld_HTR)
    HTR_MZI_ext_right.turn(width_HTR_ext/2, 'l', **ld_HTR)
    HTR_MZI_ext_right.segment(HTR_tail, '-x', **ld_HTR)
    
    # Heater on ring 1
    HTR_ring1 = gdspy.Path(width_HTR, (ring1_loc_x - ring_radius, ring1_loc_y - ring_radius))
    HTR_ring1_ext_left = gdspy.Path(width_HTR_ext, (HTR_ring1.x + width_HTR/2, HTR_ring1.y))
    HTR_ring1_ext_left.segment(HTR_tail, '-x', **ld_HTR)
    HTR_ring1.segment(0, '-y', **ld_HTR)
    HTR_ring1.turn(ring_radius, "ll", **ld_HTR)
    HTR_ring1_ext_right = gdspy.Path(width_HTR_ext, (HTR_ring1.x - width_HTR/2, HTR_ring1.y))
    HTR_ring1_ext_right.segment(HTR_tail, '+x', **ld_HTR)
    
    # Heater on ring 2
    HTR_ring2 = gdspy.Path(width_HTR, (ring2_loc_x + ring_radius, ring2_loc_y + ring_radius))
    HTR_ring2_ext_right = gdspy.Path(width_HTR_ext, (HTR_ring2.x + width_HTR/2, HTR_ring2.y))
    HTR_ring2_ext_right.segment(HTR_tail, '-x', **ld_HTR)
    HTR_ring2.segment(0, '+y', **ld_HTR)
    HTR_ring2.turn(ring_radius, "ll", **ld_HTR)
    HTR_ring2_ext_left = gdspy.Path(width_HTR_ext, (HTR_ring2.x + width_HTR/2, HTR_ring2.y))
    HTR_ring2_ext_left.segment(HTR_tail, '-x', **ld_HTR)
    
    # Heater on ring 3
    HTR_ring3 = gdspy.Path(width_HTR, (ring3_loc_x - ring_radius, ring3_loc_y - ring_radius))
    HTR_ring3_ext_left = gdspy.Path(width_HTR_ext, (HTR_ring3.x - width_HTR/2, HTR_ring3.y))
    HTR_ring3_ext_left.segment(HTR_tail, '+x', **ld_HTR)
    HTR_ring3.segment(0, '-y', **ld_HTR)
    HTR_ring3.turn(ring_radius, "ll", **ld_HTR)
    HTR_ring3_ext_right = gdspy.Path(width_HTR_ext, (HTR_ring3.x - width_HTR/2, HTR_ring3.y))
    HTR_ring3_ext_right.segment(HTR_tail, '+x', **ld_HTR)
    
    # Heater on ring 4
    HTR_ring4 = gdspy.Path(width_HTR, (ring4_loc_x + ring_radius, ring4_loc_y + ring_radius))
    HTR_ring4_ext_right = gdspy.Path(width_HTR_ext, (HTR_ring4.x - width_HTR/2, HTR_ring4.y))
    HTR_ring4_ext_right.segment(HTR_tail, '+x', **ld_HTR)
    HTR_ring4.segment(0, '+y', **ld_HTR)
    HTR_ring4.turn(ring_radius, "ll", **ld_HTR)
    HTR_ring4_ext_left = gdspy.Path(width_HTR_ext, (HTR_ring4.x + width_HTR/2, HTR_ring4.y))
    HTR_ring4_ext_left.segment(HTR_tail, '-x', **ld_HTR)
    
    #######################################################################
    # Vias
    
    # Vias parameters
    via1_type    = "Contact"
    rows1        = 4
    columns1     = 25
    via1_side    = 0.36
    via1_spacing = 0.36
    side_gap1    = 0.5
    
    via1_width  = round(columns1*via1_side + (columns1 - 1)*via1_spacing + 2*side_gap1, 3)
    via1_height = round(rows1   *via1_side + (rows1 - 1)   *via1_spacing + 2*side_gap1, 3)
    
    # MZI
    via_array_Ligentec(cell, via1_type, HTR_MZI_ext_right.x               , HTR_MZI_ext_right.y   - width_HTR_ext/2, rows1, columns1, via1_side, via1_spacing, side_gap1)
    via_array_Ligentec(cell, via1_type, HTR_MZI_ext_left.x    - via1_width, HTR_MZI_ext_left.y    - width_HTR_ext/2, rows1, columns1, via1_side, via1_spacing, side_gap1)
    # ring 1
    via_array_Ligentec(cell, via1_type, HTR_ring1_ext_right.x - via1_width, HTR_ring1_ext_right.y - width_HTR_ext/2, rows1, columns1, via1_side, via1_spacing, side_gap1)
    via_array_Ligentec(cell, via1_type, HTR_ring1_ext_left.x              , HTR_ring1_ext_left.y  - width_HTR_ext/2, rows1, columns1, via1_side, via1_spacing, side_gap1)
    # ring 2
    via_array_Ligentec(cell, via1_type, HTR_ring2_ext_right.x             , HTR_ring2_ext_right.y - width_HTR_ext/2, rows1, columns1, via1_side, via1_spacing, side_gap1)
    via_array_Ligentec(cell, via1_type, HTR_ring2_ext_left.x              , HTR_ring2_ext_left.y  - width_HTR_ext/2, rows1, columns1, via1_side, via1_spacing, side_gap1)
    # ring 3
    via_array_Ligentec(cell, via1_type, HTR_ring3_ext_right.x - via1_width, HTR_ring3_ext_right.y - width_HTR_ext/2, rows1, columns1, via1_side, via1_spacing, side_gap1)
    via_array_Ligentec(cell, via1_type, HTR_ring3_ext_left.x  - via1_width, HTR_ring3_ext_left.y  - width_HTR_ext/2, rows1, columns1, via1_side, via1_spacing, side_gap1)
    # ring 4
    via_array_Ligentec(cell, via1_type, HTR_ring4_ext_right.x - via1_width, HTR_ring4_ext_right.y - width_HTR_ext/2, rows1, columns1, via1_side, via1_spacing, side_gap1)
    via_array_Ligentec(cell, via1_type, HTR_ring4_ext_left.x              , HTR_ring4_ext_left.y  - width_HTR_ext/2, rows1, columns1, via1_side, via1_spacing, side_gap1)
    
    # #######################################################################
    # Add all paths
    cell.add(path1)
    cell.add(path2)
    cell.add(path3)
    cell.add(path4)
    cell.add(path5)
    cell.add(start_taper1)
    cell.add(start_taper2)
    cell.add(start_taper3)
    cell.add(ring1)
    cell.add(ring2)
    cell.add(ring3)
    cell.add(ring4)
    cell.add(HTR_MZI)
    cell.add(HTR_MZI_ext_left)
    cell.add(HTR_MZI_ext_right)
    cell.add(HTR_ring1)
    cell.add(HTR_ring2)
    cell.add(HTR_ring3)
    cell.add(HTR_ring4)
    cell.add(HTR_ring1_ext_left)
    cell.add(HTR_ring1_ext_right)
    cell.add(HTR_ring2_ext_left)
    cell.add(HTR_ring2_ext_right)
    cell.add(HTR_ring3_ext_left)
    cell.add(HTR_ring3_ext_right)
    cell.add(HTR_ring4_ext_left)
    cell.add(HTR_ring4_ext_right)

gdspy.LayoutViewer(lib)
if overwrite == 1:
    lib.write_gds("elliptical_Ligentec.gds")

gdspy.current_library = gdspy.GdsLibrary()




#/data/tower/ph18/HOTCODE/amslibs/cds_oa/cdslibs/ph18/devices/devices_ph18mx/ph18.layermap