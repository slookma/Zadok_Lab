# -*- coding: utf-8 -*-
"""
Created on Mon May 29 14:15:06 2023

@author: benamis9
"""

def s_coupler(cell, coupling_length, x=0, y=0, coupling_dis=0.3, L_sbend=80.0, H_sbend=40.0, top=True, layer_wg={"layer": 174, "datatype": 0}):
    """
    important - the distance between the paths before the funcion is used need to be 1.5*H_sbend + coupling_dis + wg_width
    
    param: cell: the cell we are working on
    param coupling_length: as it sounds...
    
    param x: starting point on x_axis of the bottom WG
    param y: starting point on y_axis of the bottom WG
    param coupling_dis: distance between WG in coupler
    param L_sbend: the length of every S_bend
    param H_sbend: the height of every S_bend
    param: top: boolean - if True start from top
    param layer_wg: what layer we want our WG in

    :return: location of the end of the WG 
    for example a=scoupler()
    a[0] =bottom WG coardenits (x,y)
    a[1] =top WG coardenits (x,y)
    
    """
    
    # import
    import gdspy
    import numpy as np

    # creating s_bend from David Trop
    def sbendPath(wgsbend, L=L_sbend, H=H_sbend, layer_1 = layer_wg):
        # the formula for cosine-shaped s-bend is: y(x) = H/2 * [1- cos(xpi/L)]
        # the formula for sine-shaped s-bend is: y(x) = xH/L - H/(2pi) * sin(x2*pi/L)
        def sbend(t):
            y = H / 2 * (1 - np.cos(t * np.pi))
            x = L * t

            return (x, y)

        def dtsbend(t):
            dy_dt = H / 2 * np.pi * np.sin(t * np.pi)
            dx_dt = L

            return (dx_dt, dy_dt)

        wgsbend.parametric(sbend, dtsbend, number_of_evaluations=100,**layer_1)
        return wgsbend

    def sbendPathM(wgsbend, L=L_sbend, H=H_sbend, layer_1 = layer_wg):
        # the formula for cosine-shaped s-bend is: y(x) = H/2 * [1- cos(xpi/L)]
        # the formula for sine-shaped s-bend is: y(x) = xH/L - H/(2pi) * sin(x2*pi/L)
        def sbend(t):
            y = H / 2 * (np.cos(t * np.pi))
            x = L * t

            return (x, y)

        def dtsbend(t):
            dy_dt = -H / 2 * np.pi * np.sin(t * np.pi)
            dx_dt = L

            return (dx_dt, dy_dt)

        wgsbend.parametric(sbend, dtsbend, number_of_evaluations=100,**layer_1)
        return wgsbend

    # starting point defualt
    # x=0
    # y = 0


    ## create paths

    path1 = gdspy.Path(1, (x, y))
    if top:
        # start from top
        path3 = gdspy.Path(1, (path1.x, path1.y - 1.5 * H_sbend - coupling_dis-1))

        path1 = sbendPathM(path1)
        path1.segment(coupling_length)
        path1 = sbendPath(path1)

        path3 = sbendPath(path3)
        path3.segment(coupling_length)

        path2 = gdspy.Path(1, (path3.x, path3.y - H_sbend / 2))
    else:
        # start from bottom
        path3 = gdspy.Path(1, (path1.x, path1.y + 1 + 1.5 * H_sbend + coupling_dis))
        # bottom WG
        path1 = sbendPath(path1)
        path1.segment(coupling_length)
        path2 = gdspy.Path(1, (path1.x, path1.y - H_sbend / 2))
        path2 = sbendPathM(path2)
        # top WG
        path3 = sbendPathM(path3)
        path3.segment(coupling_length)
        path3 = sbendPath(path3)
        
    # adding to design
    cell.add(path1)
    cell.add(path2)
    cell.add(path3)

    (x_bot, y_bot) = (path2.x, path2.y)
    (x_top, y_top) = (path3.x, path3.y)

    return [(x_bot, y_bot), (x_top, y_top)]