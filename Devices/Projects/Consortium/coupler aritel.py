import gdspy
import numpy as np

# GDS starting
lib = gdspy.GdsLibrary()
design = lib.new_cell('coupler')

# Layer definitions
layer_wg = {"layer": 174, "datatype": 0}
layer_heater = {"layer": 26, "datatype": 0}

# Parameters
rad = 80
H_sbend = rad/2
L_sbend = 3*H_sbend
lc = 400
taper = 0.3
chip_size = 4980
coupling_dis = 0.2
wg_width = 1
taper_length = 300
heater_w = 5
heater_l = 300
test_length = 5
array_dis = 127
# S-bend functions
def sbendPath_x(wgsbend, L=L_sbend, H=H_sbend, layer_1=layer_wg):
    def sbend(t):
        y = H / 2 * (1 - np.cos(t * np.pi))
        x = L * t
        return (x, y)

    def dtsbend(t):
        dy_dt = H / 2 * np.pi * np.sin(t * np.pi)
        dx_dt = L
        return (dx_dt, dy_dt)

    wgsbend.parametric(sbend, dtsbend, number_of_evaluations=100, **layer_1)
    return wgsbend


def sbendPathM_x(wgsbend, L=L_sbend, H=H_sbend, layer_1=layer_wg):
    def sbend(t):
        y = -H / 2 * (1 - np.cos(t * np.pi))
        x = L * t
        return (x, y)

    def dtsbend(t):
        dy_dt = -H / 2 * np.pi * np.sin(t * np.pi)
        dx_dt = L
        return (dx_dt, dy_dt)

    wgsbend.parametric(sbend, dtsbend, number_of_evaluations=100, **layer_1)
    return wgsbend


def create_sbend_sequence(top, bot, lc, H_sbend, layer_wg, heater_w, layer_heater, cell, L=L_sbend):
    sbendPathM_x(top, L, H_sbend, layer_wg)
    sbendPath_x(bot, L, H_sbend, layer_wg)

    heater = gdspy.Path(heater_w, initial_point=(top.x, (top.y + bot.y) / 2))
    heater.segment(lc, **layer_heater)
    cell.add(heater)

    top.segment(lc, **layer_wg)
    bot.segment(lc, **layer_wg)

    sbendPath_x(top, L, H_sbend, layer_wg)
    sbendPathM_x(bot, L, H_sbend, layer_wg)


def rotations(path, rotations_array, rad, layer):
    for rotation in rotations_array:
        if type(rotation) is str:
            path.turn(rad, rotation, **layer)
        else:
            path.segment(rotation, **layer)
    return path


def create_and_add_heater(top, bot, rad, heater_w, layer_wg, layer_heater, cell, opt="A"):
    rotations_array_A = ["ll", "l", "r", lc, "r", rad / 2, "r", 1.5*lc + 2.5 * rad, "r", rad / 2, "l"]
    rotations_array_B = rotations_array_A[::-1]
    heater = gdspy.Path(heater_w, initial_point=(bot.x, bot.y))
    if opt == "A":
        rotations(top, rotations_array_A, rad=rad, layer=layer_wg)
        heater.segment(lc, **layer_heater)

    elif opt == "B":
        rotations(top, rotations_array_A, rad=rad, layer=layer_wg)
        rotations(top, rotations_array_B, rad=rad, layer=layer_wg)
        heater.segment(lc, **layer_heater)
    else:
        raise ValueError("Invalid option. Choose 'A' or 'B'.")

    bot.segment(top.x - bot.x, **layer_wg)
    cell.add(heater)
    return heater.x

top = gdspy.Path(taper)
bot = gdspy.Path(taper, (0, -(2 * H_sbend + coupling_dis + wg_width)))

top.segment(taper_length, final_width=wg_width, **layer_wg)
bot.segment(taper_length, final_width=wg_width, **layer_wg)
# coupler
create_sbend_sequence(top, bot, lc, H_sbend, layer_wg, heater_w, layer_heater, design)
# tau
heater1_end = create_and_add_heater(top, bot, rad, heater_w, layer_wg, layer_heater, design, opt="A")
tau = top.length-bot.length
print(tau)
# coupler
create_sbend_sequence(top, bot, lc, H_sbend, layer_wg, heater_w, layer_heater, design)
# 2 tau
heater2_end = create_and_add_heater(top, bot, rad, heater_w, layer_wg, layer_heater, design, opt="B")
tau2 = top.length-bot.length-tau
print(tau2)
# coupler
create_sbend_sequence(top, bot, lc, H_sbend, layer_wg, heater_w, layer_heater, design)
# taper out
sbendPath_x(top, 2*L_sbend, array_dis-(top.y-bot.y), layer_wg)
top.segment(chip_size-top.x-taper_length, **layer_wg).segment(taper_length, final_width=taper, **layer_wg)
bot.segment(chip_size-bot.x-taper_length, **layer_wg).segment(taper_length, final_width=taper, **layer_wg)
design.add(top).add(bot)

# test ports
test1 = gdspy.Path(taper, (0, top.y-(array_dis+ coupling_dis)))
test1.segment(taper_length, final_width=wg_width, **layer_wg).segment(heater2_end-taper_length, **layer_wg)
sbendPath_x(test1, 0.5*L_sbend, bot.y - (test1.y + coupling_dis), layer_wg)
test1.segment(test_length, **layer_wg)
sbendPathM_x(test1, 0.5*L_sbend, H_sbend, layer_wg)
test1.segment(chip_size-test1.x-taper_length, **layer_wg).segment(taper_length, final_width=taper, **layer_wg)

test4 = gdspy.Path(taper, (0, bot.y+3*array_dis + coupling_dis))
test4.segment(taper_length, final_width=wg_width, **layer_wg).segment(heater1_end-2*lc, **layer_wg)
test4_dis = test4.y-(top.y+2.5*rad+coupling_dis+wg_width)
sbendPathM_x(test4, L_sbend, test4_dis, layer_wg)
test4.segment(test_length, **layer_wg)
sbendPath_x(test4, L_sbend, test4_dis, layer_wg)
test4.segment(chip_size-test4.x-taper_length, **layer_wg).segment(taper_length, final_width=taper, **layer_wg)



design.add(test1).add(test4)
lib.write_gds('ariel_coupler.gds')
