# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 11:33:14 2023

@author: benamis9
"""

# Units: um

import numpy as np
import gdspy
import math


overwrite   = 0 # 1 - Overwrite GDS, 0 - Don't overwrite
lib = gdspy.GdsLibrary()
cell = lib.new_cell('HUJI_50_50_coup_U')

# Parameters:
txtSize             = 50
width               = 0.7
coup_gap            = 0.3 + width
W_gc                = 100
xGap                = 400
x_run_start         = 300
chip_size           = 10000
U_pitch_start       = 120
U_pitch_stop        = 130
Lc_start            = 15
Lc_stop             = 25
max_bend_radius     = U_pitch_stop / 2
tot_width           = 7*max_bend_radius + Lc_stop + x_run_start - coup_gap + W_gc + xGap
U_pitch_vec         = np.linspace(U_pitch_start, U_pitch_stop, math.floor((chip_size - 1000) / tot_width))

for idx_U in range(len(U_pitch_vec)):
    U_pitch             = U_pitch_vec[idx_U]
    bend_radius         = U_pitch / 2
    tot_height          = 6 * U_pitch
    Lc_vec              = np.linspace(Lc_start, Lc_stop, math.floor((chip_size - 1000) / tot_height))
    
    
    for idx_Lc in range(len(Lc_vec)):
        Lc = Lc_vec[idx_Lc]
        ###########################################################################
        # Start path1 (Bottom U shape)
        path1 = gdspy.Path(width, (tot_width * idx_U, tot_height * idx_Lc))
        x_start = path1.x
        y_start = path1.y
        path1.segment(x_run_start, "+x")
        path1.turn(bend_radius, "ll")
        path1.segment(x_run_start)
        ###########################################################################
        # Start path2 (Bottom coupler branch)
        path2 = gdspy.Path(width, (tot_width * idx_U, tot_height * idx_Lc + 2 * U_pitch))
        path2.segment(x_run_start + bend_radius, "+x")
        path2.turn(bend_radius, "r")
        path2.turn(bend_radius, "l")
        path2.segment(3*bend_radius - coup_gap + Lc)
        path2.turn(bend_radius, "l")
        path2.segment(3*bend_radius)
        path2.turn(bend_radius - coup_gap/2, "l")
        txtPosX = path2.x
        txtPosY = path2.y
        path2.segment(Lc)
        path2.turn(bend_radius - coup_gap/2, "l")
        path2.segment(bend_radius)
        path2.turn(bend_radius, "rr")
        path2.turn(bend_radius, "l")
        path2.segment(x_run_start + 2*bend_radius)
        ###########################################################################
        # Start path3 (Upper coupler branch)
        path3 = gdspy.Path(width, (tot_width * idx_U, tot_height * idx_Lc + 4 * U_pitch))
        path3.segment(x_run_start + 2*bend_radius, "+x")
        path3.turn(bend_radius, "l")
        path3.turn(bend_radius, "rr")
        path3.segment(bend_radius)
        path3.turn(bend_radius - coup_gap/2, "l")
        path3.segment(Lc)
        path3.turn(bend_radius - coup_gap/2, "l")
        path3.segment(3*bend_radius)
        path3.turn(bend_radius, "l")
        path3.segment(3*bend_radius - coup_gap + Lc)
        path3.turn(bend_radius, "l")
        path3.turn(bend_radius, "r")
        path3.segment(x_run_start + bend_radius)
        ###########################################################################
        # Start path4 (Upper U shape)
        if idx_Lc == len(Lc_vec)-1:
            path4 = gdspy.Path(width, (tot_width * idx_U, tot_height * idx_Lc + tot_height))
            path4.segment(x_run_start, "+x")
            path4.turn(bend_radius, "ll")
            path4.segment(x_run_start)
        
        txt = gdspy.Text(f"Lc = {Lc:{2}.{4}} um", txtSize*0.7, position=(txtPosX + 2*bend_radius, txtPosY + 4*bend_radius), angle=3*np.pi/2)
        cell.add(path1)
        cell.add(path2)
        cell.add(path3)
        cell.add(txt)
    
    txt = gdspy.Text(f"pitch = {U_pitch:{2}.{4}} um", txtSize, position=(tot_width * idx_U, -txtSize*2))
    cell.add(path4)
    cell.add(txt)
    


gdspy.LayoutViewer(lib)
if overwrite == 1:
    lib.write_gds("HUJI_50_50_coup_U.gds")

# Enable running on the same kernel
gdspy.current_library = gdspy.GdsLibrary()