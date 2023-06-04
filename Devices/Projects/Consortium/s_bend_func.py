
import gdspy
import numpy as np

# gds starting
lib = gdspy.GdsLibrary()
cell = lib.new_cell('sbend_func')
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
