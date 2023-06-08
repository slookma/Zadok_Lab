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

    path_top = sbendPathM(path_top)
    path_top.segment(coupling_length, **layer_wg)
    path_top = sbendPath(path_top)

    path_bot = sbendPath(path_bot)
    path_bot.segment(coupling_length, **layer_wg)
    path_bot = sbendPathM(path_bot)

    return [path_bot, path_top]


def fix_x(path1, path2):
    dx = path1.x - path2.x
    if dx < 0:
        path1.segment(abs(dx), **layer_wg)
    else:
        path2.segment(abs(dx), **layer_wg)


def fix_y(path1, path2, wanted_dis):
    # figure top and bottom
    if path1.y > path2.y:
        top_path = path1
        bot_path = path2
    else:
        top_path = path2
        bot_path = path1
    # fix placing using s shape
    dy = abs(top_path.y - bot_path.y)
    fix = abs(dy - wanted_dis)
    if dy < wanted_dis:
        bot_path = sbendPathM(bot_path, 3 * fix, fix)
    else:
        bot_path = sbendPath(bot_path, 3 * fix, fix)
    top_path.segment(3 * fix, **layer_wg)

    return [top_path, bot_path]


def fix_dis(path1, path2, wanted_dis):
    fix_x(path1, path2)
    return fix_y(path1, path2, wanted_dis)


def mzi(cell, path1, path2, coupling_length,
        coupling_dis=0.3, wg_dis=30, wg_width=1 , Hsbend=40, taper=0.3, size=5000):
    """

    :param cell:cell
    :param taper: 0.3
    :param path1 / 2 the WG coming in
    :param size: size of chip
    :return:x place at end of mzi
    """
    # path dis fix
    dy = abs(path1.y - path2.y)
    paths = fix_dis(path1, path2, 2 * H_sbend + coupling_dis + wg_width)
    ## MZI
    # coupler
    coupler1 = s_coupler(cell, paths[0], paths[1], coupling_length)
    # length difference
    paths[1].segment(2*L_sbend, **layer_wg)
    paths[0] = sbendPathM(coupler1[1])
    paths[0] = sbendPath(coupler1[1])
    # coupler 2
    coupler2 = s_coupler(cell, paths[0], paths[1], coupling_length)
    # move paths to top - same distance as input
    paths[1] = sbendPath(paths[1], 3*(2*Hsbend-wg_dis+wg_width+coupling_dis),
                         2*Hsbend-dy+wg_width+coupling_dis)
    paths[0].segment(3*(2*Hsbend-wg_dis+wg_width+coupling_dis), **layer_wg)
    # return paths if wanted
    return paths[0], paths[1]


lib.write_gds('mzi2.gds')
