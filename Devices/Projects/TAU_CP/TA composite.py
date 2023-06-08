import gdspy
import numpy

# gds starting
lib = gdspy.GdsLibrary()
cell = lib.new_cell('TA')
# S bend parameters
L_sbend = 80.0
H_sbend = 40.0
# dis between WG when coupling
coupling_dis = 0.3
# width of WG
wg_width = 1
# layer
layer_wg = {"layer": 174, "datatype": 0}

path1 = gdspy.Path(1)
path2 = gdspy.Path(1, (0, 403))

r = 80


def r_coupler(path1, path2, radios_turn, path1_seg:list, path1_length:list,
              path2_seg=None, path2_length=None):
    if not isinstance(path1_seg, list):
        raise TypeError("path1_seg must be a list.")
    # figure top and bottom
    if path1.y > path2.y:
        top_path = path1
        bot_path = path2
    else:
        top_path = path2
        bot_path = path1
    # turn to place
    top_path.turn(radios_turn, 'r').turn(radios_turn, 'l')
    bot_path.turn(radios_turn, 'l').turn(radios_turn, 'r')
    # changing width top WG
    for i in range(len(path1_seg) - 1):
        top_path.segment(path1_length[i]).segment(1, final_width=path1_seg[i+1])
    top_path.segment(path1_seg[-1])
    # changing width bottom WG
    bot_x = bot_path.x
    if path2_seg:
        for i in range(len(path2_seg) - 1):
            bot_path.segment(path2_length[i]).segment(1, final_width=path2_seg[i + 1])
        bot_path.segment(path2_seg[-1])
    else:
        bot_path.segment(top_path.x - bot_x)
    top_path.turn(radios_turn, 'l').turn(radios_turn, 'rr').\
        turn(radios_turn, 'll').turn(radios_turn, 'rr').turn(radios_turn, 'l')
    bot_path.turn(radios_turn, 'r').turn(radios_turn, 'l').\
        segment(4*radios_turn).turn(radios_turn, 'l').turn(radios_turn, 'r')
    # changing width top WG
    for i in range(len(path1_seg) - 1):
        top_path.segment(path1_length[i]).segment(1, final_width=path1_seg[i+1])
    top_path.segment(path1_seg[-1])
    # changing width bottom WG
    bot_x = bot_path.x
    if path2_seg:
        for i in range(len(path2_seg) - 1):
            bot_path.segment(path2_length[i]).segment(1, final_width=path2_seg[i + 1])
        bot_path.segment(path2_seg[-1])
    else:
        bot_path.segment(top_path.x - bot_x)
    top_path.turn(radios_turn, 'l').turn(radios_turn, 'r')
    bot_path.turn(radios_turn, 'r').turn(radios_turn, 'l')
# path1.segment(100)
# path1.turn(r, 'l').turn(r, 'rr').turn(r, 'll').turn(r, 'rr').turn(r, 'l')
# path1.segment(100)
# path1.turn(r, 'r').turn(r, 'l').segment(400).turn(r, 'l').turn(r,'rr').turn(r, 'l')
# path2.segment(100)
# top_path = path2
path1_w = [0.5, 1, 0.5, 2, 0.1]
path1_l = [50, 10, 20, 50, 10]
r_coupler(path1, path2, 100, path1_w, path1_l, path1_w, path1_l)
cell.add(path1)
cell.add(path2)

lib.write_gds('TA.gds')