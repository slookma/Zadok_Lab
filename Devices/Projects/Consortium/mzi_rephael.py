# -*- coding: utf-8 -*-
"""
Created on Mon May 29 13:41:32 2023

@author: sunaraf
"""

import gdspy
import numpy as np

# gds starting
lib = gdspy.GdsLibrary()
cell = lib.new_cell('mzi_1')
# S bend parameters
L_sbend = 110.0
H_sbend = 40.0
# dis between WG when coupling
coupling_dis = 0.3
# width of WG
wg_width = 1
# layer
layer_wg = {"layer": 174, "datatype": 0}


# creating s_bend from David Trop
def sbendPath(wgsbend, L=L_sbend, H=H_sbend, layer_1=layer_wg):
    # the formula for cosine-shaped s-bend is: y(x) = H/2 * [1- cos(xpi/L)]
    # the formula for sine-shaped s-bend is: y(x) = xH/L - H/(2pi) * sin(x2*pi/L)
    def sbend(t):
        # y = H / 2 * (1 - np.cos(t * np.pi))
        y = H / 2 * (1 - np.cos(t * np.pi))
        x = L * t

        return (x, y)

    def dtsbend(t):
        dy_dt = H / 2 * np.pi * np.sin(t * np.pi)
        dx_dt = L

        return (dx_dt, dy_dt)

    wgsbend.parametric(sbend, dtsbend, number_of_evaluations=100, **layer_1)
    return wgsbend

def sbendPathM(wgsbend, L=L_sbend, H=H_sbend, layer_1=layer_wg):
    # the formula for cosine-shaped s-bend is: y(x) = H/2 * [1- cos(xpi/L)]
    # the formula for sine-shaped s-bend is: y(x) = xH/L - H/(2pi) * sin(x2*pi/L)
    def sbend(t):
        # y = -H / 2 * (np.cos(t * np.pi))
        y = -H / 2 * (1 - np.cos(t * np.pi))
        x = L * t

        return (x, y)

    def dtsbend(t):
        dy_dt = -H / 2 * np.pi * np.sin(t * np.pi)
        dx_dt = L

        return (dx_dt, dy_dt)

    wgsbend.parametric(sbend, dtsbend, number_of_evaluations=100, **layer_1)
    return wgsbend

def s_coupler(cell, path_top, path_bot, coupling_length):
    """

    IMPORTENT - THE DISTANCE OF PATHS NEEDS TO BE (2 * H_sbend + coupling_dis + wg_width)

    :param cell:cell we are writing on
    :param path_top: the path of the top WG
    :param path_bot: the path of the bot WG
    :param coupling_length: as it sounds
    :return: [path_bot, path_top]
    """
    # import
    import gdspy
    import numpy as np
    ## create paths

    path_top = sbendPathM(path_top)
    path_top.segment(coupling_length, **layer_wg)
    path_top = sbendPath(path_top)

    path_bot = sbendPath(path_bot)
    path_bot.segment(coupling_length, **layer_wg)
    path_bot = sbendPathM(path_bot)

    return [path_bot, path_top]

def mzi(cell, mzi1_top, mzi1_bot, coupling_length, coupling_dis=0.3, wg_dis=30, wg_width=1 , Hsbend=40, taper=0.3, size=5000):
    """

    :param cell:cell
    :param taper: 0.3
    :param mzi1_top: top WG
    :param mzi1_bot: bottom WG
    :param size: size of chip
    :return:x place at end of mzi
    """
    # path dis fix
    mzi1_top = sbendPath(mzi1_top, 2.5*(2*Hsbend-wg_dis+wg_width+coupling_dis), 2*Hsbend-wg_dis+wg_width+coupling_dis)
    mzi1_bot.segment(2.5*(2*Hsbend-wg_dis+wg_width+coupling_dis), **layer_wg)
    ## MZI
    # coupler
    coupler1 = s_coupler(cell, mzi1_top, mzi1_bot, coupling_length)
    # length difrence
    mzi1_bot.segment(2*L_sbend, **layer_wg)
    mzi1_top = sbendPathM(coupler1[1])
    mzi1_top = sbendPath(coupler1[1])
    # coupler 2
    coupler2 = s_coupler(cell, mzi1_top, mzi1_bot, coupling_length)
    mzi1_bot = sbendPath(mzi1_bot, 2.5*(2*Hsbend-wg_dis+wg_width+coupling_dis), 2*Hsbend-wg_dis+wg_width+coupling_dis)
    mzi1_top.segment(2.5*(2*Hsbend-wg_dis+wg_width+coupling_dis), **layer_wg)
    # return x place
    x = mzi1_top.x
    # add WG to end of chip
    mzi1_top.segment(size-mzi1_top.x-100, **layer_wg)
    mzi1_bot.segment(size-mzi1_bot.x-100, **layer_wg)
    # taper
    mzi1_bot.segment(100, final_width=taper, **layer_wg)
    mzi1_top.segment(100, final_width=taper, **layer_wg)
    # add to cell
    cell.add(mzi1_bot)
    cell.add(mzi1_top)

def create_ring(cell, path1, coupling_dis, wg_width, bend_radius, top_bot=True):
    if top_bot:
        direction = "ll"
        y_start = path1.y + coupling_dis + wg_width
    else:
        direction = "rr"
        y_start = path1.y - (coupling_dis + wg_width)

    ring_path = gdspy.Path(wg_width, (path1.x, y_start))
    ring_path.segment(coupling_length)
    ring_path.turn(bend_radius, direction)
    ring_path.segment(coupling_length)
    ring_path.turn(bend_radius, direction)

    cell.add(ring_path)
coupling_length=0
# path2 = gdspy.Path(1)
# create_ring(cell, path2, 0, 1, 80)
start_x = 0
start_y = -100
j = 0
MZI_size = 900

CL = [0,6,8,10,11.85,14, 18, 20, 24, 26, 28,29,32,34,36,50,56,59]
for i in range(len(CL)):
    # starting point
    if j==5:
        j = 0
        start_y = start_y - 50

    wg_dis = 30
    wg_width = 1
    taper = 0.3

    # create path
    mzi_top = gdspy.Path(taper, (0, start_y-i*wg_dis))
    mzi_bot = gdspy.Path(taper, (0, start_y-(i+1)*wg_dis))
    # taper
    mzi_bot.segment(100, final_width=wg_width, **layer_wg)
    mzi_top.segment(100, final_width=wg_width, **layer_wg)

    # add wg to MZI starting point
    mzi_bot.segment(j*MZI_size, **layer_wg)
    mzi_top.segment(j * MZI_size, **layer_wg)
    #
    mzi(cell, mzi_top, mzi_bot, CL[i], wg_dis=wg_dis, size=4980)
    start_y = start_y-1*wg_dis
    j += 1
#lib.write_gds('mzi1064.gds')
gdspy.LayoutViewer(lib)
gdspy.current_library = gdspy.GdsLibrary()