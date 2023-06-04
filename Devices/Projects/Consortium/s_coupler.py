import gdspy
import numpy as np

# gds starting
lib = gdspy.GdsLibrary()
cell = lib.new_cell('s_coupler')
# S bend parameters
L_sbend = 80.0
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
    path_top.segment(coupling_length)
    path_top = sbendPath(path_top)

    path_bot = sbendPath(path_bot)
    path_bot.segment(coupling_length)
    path_bot = sbendPathM(path_bot)

    return [path_bot, path_top]
