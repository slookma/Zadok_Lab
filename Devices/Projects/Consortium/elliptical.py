# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Units: um

import numpy
import gdspy

overwrite = 0 # 1 - Overwrite GDS, 0 - Don't overwrite
lib = gdspy.GdsLibrary()
cell = lib.new_cell('Elliptical_Filter')


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
width               = 1
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
# Lc_D3_vec           = [4.95, 14.15, 10.75, 19.95]
# Lc_D4_vec           = [9.65, 18.85, 6.81, 15.9]
Lc_D3_vec           = [4.95,  6,  7,  8,  9, 10, 11, 12, 14.15]
Lc_D4_vec           = [9.65, 11, 12, 13, 14, 15, 16, 17, 18.85]
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
    # Start path8 (ring1 bottom) - NWG + TNR cover
    path8 = gdspy.Path(width, (x_ring1_bottom, y_ring1_bottom + coup_gap + width))
    path8.turn(ring_radius, "ll", **ld_NWG)
    path8.segment(Lc_D3, **ld_NWG)
    path8.turn(ring_radius, "ll", **ld_NWG)
    path8.segment(Lc_D3, **ld_NWG)
    
    path12 = gdspy.Path(width*2, (x_ring1_bottom + ring_radius, y_ring1_bottom + ring_radius + coup_gap + width))
    path12.segment(0, '+y', **ld_TNR)
    path12.turn(ring_radius, "l", **ld_TNR)
    path12.segment(Lc_D3, **ld_TNR)
    path12.turn(ring_radius, "l", **ld_TNR)
    
    #######################################################################
    # Start path9 (ring2 bottom) - NWG + TNR cover
    path9 = gdspy.Path(width, (x_ring2_bottom, y_ring2_bottom + coup_gap + width))
    path9.turn(ring_radius, "ll", **ld_NWG)
    path9.segment(Lc_D4, **ld_NWG)
    path9.turn(ring_radius, "ll", **ld_NWG)
    path9.segment(Lc_D4, **ld_NWG)
    
    path13 = gdspy.Path(width*2, (x_ring2_bottom + ring_radius, y_ring2_bottom + ring_radius + coup_gap + width))
    path13.segment(0, '+y', **ld_TNR)
    path13.turn(ring_radius, "l", **ld_TNR)
    path13.segment(Lc_D3, **ld_TNR)
    path13.turn(ring_radius, "l", **ld_TNR)
    
    #######################################################################
    # Start path10 (ring1 top) - NWG + TNR cover
    path10 = gdspy.Path(width, (x_ring1_top, y_ring1_top - coup_gap - width))
    path10.turn(ring_radius, "rr", **ld_NWG)
    path10.segment(Lc_D3, **ld_NWG)
    path10.turn(ring_radius, "rr", **ld_NWG)
    path10.segment(Lc_D3, **ld_NWG)
    
    path14 = gdspy.Path(width*2, (x_ring1_top + ring_radius, y_ring1_top - ring_radius - coup_gap - width))
    path14.segment(0, '-y', **ld_TNR)
    path14.turn(ring_radius, "r", **ld_TNR)
    path14.segment(Lc_D3, **ld_TNR)
    path14.turn(ring_radius, "r", **ld_TNR)
    
    #######################################################################
    # Start path11 (ring2 top) - NWG + TNR cover
    path11 = gdspy.Path(width, (x_ring2_top, y_ring2_top - coup_gap - width))
    path11.turn(ring_radius, "rr", **ld_NWG)
    path11.segment(Lc_D4, **ld_NWG)
    path11.turn(ring_radius, "rr", **ld_NWG)
    path11.segment(Lc_D4, **ld_NWG)
    
    path15 = gdspy.Path(width*2, (x_ring2_top + ring_radius, y_ring2_top - ring_radius - coup_gap - width))
    path15.segment(0, '-y', **ld_TNR)
    path15.turn(ring_radius, "r", **ld_TNR)
    path15.segment(Lc_D3, **ld_TNR)
    path15.turn(ring_radius, "r", **ld_TNR)
    
    
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
    cell.add(start_taper)

gdspy.LayoutViewer(lib)
if overwrite == 1:
    lib.write_gds("elliptical.gds")

gdspy.current_library = gdspy.GdsLibrary()