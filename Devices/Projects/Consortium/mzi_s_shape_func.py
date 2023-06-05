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
    y_fix = mzi1_top.y - mzi1_bot.y
    if y_fix - (2 * H_sbend + coupling_dis + wg_width) < 0:
        mzi1_top = sbendPath(mzi1_top, 3 * ((2 * H_sbend + coupling_dis + wg_width) - y_fix),
                             (2 * H_sbend + coupling_dis + wg_width) - y_fix)
    x_fix = mzi1_top.x - mzi1_bot.x
    if x_fix < 0:
        mzi1_top.segment(-x_fix, **layer_wg)
    else:
        mzi1_bot.segment(x_fix, **layer_wg)

    ## MZI
    # coupler
    coupler1 = s_coupler(cell, mzi1_top, mzi1_bot, coupling_length)
    # length difrence
    mzi1_bot.segment(2*L_sbend, **layer_wg)
    mzi1_top = sbendPathM(coupler1[1])
    mzi1_top = sbendPath(coupler1[1])
    # coupler 2
    coupler2 = s_coupler(cell, mzi1_top, mzi1_bot, coupling_length)
    # move paths to top - same distance as input
    mzi1_bot = sbendPath(mzi1_bot, 3*(2*Hsbend-wg_dis+wg_width+coupling_dis), 2*Hsbend-y_fix+wg_width+coupling_dis )
    mzi1_top.segment(3*(2*Hsbend-wg_dis+wg_width+coupling_dis), **layer_wg)
    # return paths if wanted
    return mzi1_top, mzi1_bot


lib.write_gds('mzi2.gds')
