import gdspy
import numpy

# gds starting
lib = gdspy.GdsLibrary()
cell = lib.new_cell('TA')

# dis between WG when coupling
coupling_dis = 0.3
# width of WG
wg_width = 1
# layer
layer_wg = {"layer": 174, "datatype": 0}


def composite_mzi(cell, path1, path2, radios_turn, path1_seg: list, path1_length: list,
                  path2_seg=None, path2_length=None, text=None, core=True,
                  layer={"layer": 0, "datatype": 0}):
    # 1. Initialize the paths
    top_path, bot_path = initialize(path1, path2, path1_seg)

    # 2. Coupler 1
    coupler(top_path, bot_path, radios_turn, path1_seg, path1_length, path2_seg, path2_length, core=core, layer=layer)

    # 3. Add text
    add_text(cell, top_path, text, layer=layer)

    # 4. Optical distance of paths
    rotate_paths(top_path, radios_turn, [4 * radios_turn], layer=layer)
    rotate_paths(bot_path, radios_turn, ['l', 'rr', 'l'], layer=layer)

    # 5. Coupler 2 (same as Coupler 1)
    coupler(top_path, bot_path, radios_turn, path1_seg, path1_length, path2_seg, path2_length, core=core, layer=layer)


def initialize(path1, path2, path1_seg: list):
    if not isinstance(path1_seg, list):
        raise TypeError("path1_seg must be a list.")

    # Determine the top and bottom paths based on their y-coordinate
    if path1.y > path2.y:
        top_path, bot_path = path1, path2
    else:
        top_path, bot_path = path2, path1

    return top_path, bot_path


def coupler(top_path, bot_path, radios_turn, path1_seg: list, path1_length: list,
            path2_seg=None, path2_length=None, core=True, layer={"layer": 0, "datatype": 0}):
    # Rotate the top and bottom paths to their final positions
    rotate_paths(top_path, radios_turn, ['r', 'l'], layer=layer)
    rotate_paths(bot_path, radios_turn, ['l', 'r'], layer=layer)

    # Change the width of the top and bottom paths
    change_width(top_path, path1_seg, path1_length, core=core, layer=layer)

    if path2_seg:
        change_width(bot_path, path2_seg, path2_length, layer=layer)
    else:
        bot_path.segment(top_path.x - bot_path.x, **layer)
    if top_path.x != bot_path.x:
        raise TypeError("Wave guides in offset")

    # Rotate the top and bottom paths to their final positions
    rotate_paths(top_path, radios_turn, ['l', 'r'], layer=layer)
    rotate_paths(bot_path, radios_turn, ['r', 'l'], layer=layer)


def add_text(cell, top_path, text, layer={"layer": 0, "datatype": 0}):
    if text:
        labeling = gdspy.Text(text, 40, (top_path.x, top_path.y + 10), **layer)
        cell.add(labeling)


def rotate_paths(path, radios_turn, rotations, layer={"layer": 0, "datatype": 0}):
    # Rotate the path
    for rotation in rotations:
        if isinstance(rotation, str):
            path.turn(radios_turn, rotation, **layer)
        else:
            path.segment(rotation, **layer)


def change_width(path, path_seg, path_length, core=True, layer={"layer": 0, "datatype": 0}):
    # Add taper at the start
    if core:
        path.segment(1, final_width=0.4, **layer)
    else:
        path.segment(1, **layer)

    # Change the width of the path segments based on the given lengths
    for i in range(len(path_seg)):
        path.segment(1, final_width=path_seg[i], **layer).segment(path_length[i], **layer)

    # Add taper at the end
    if core:
        path.segment(1, final_width=0.7, **layer)
    else:
        path.segment(1, **layer)


def mzi_clad(cell, path1, path2, radios_turn, path1_seg: list, path1_length: list,
                  path2_seg=None, path2_length=None, text=None,
                  layer={"layer": 0, "datatype": 0}):
    clad_p1 = gdspy.Path(5, (path1.x, path1.y))
    clad_p2 = gdspy.Path(5, (path2.x, path2.y))

    composite_mzi(cell, path1, path2, radios_turn, path1_seg, path1_length,
                  path2_seg, path2_length, text=text, layer=layer_wg)
    composite_mzi(cell, clad_p1, clad_p2, radios_turn, [5] * len(path1_length),
                  path1_length, core=False)

    inv1 = gdspy.boolean(path1, clad_p1, "xor")
    inv2 = gdspy.boolean(path2, clad_p2, "xor")

    cell.add(inv1)
    cell.add(inv2)

# # example
# path11 = gdspy.Path(0.7)
# path22 = gdspy.Path(0.7, (0, 403))
#
# path1_w = [0.1, 3, 0.5, 2, 0.1]
# path1_l = [10, 10, 20, 50, 10]
#
# path2_w = [2, 1, 0.5, 1, 2]
# path2_l = [10, 10, 20, 50, 10]
# path3 = gdspy.Path(5)
# path4 = gdspy.Path(5, (0, 403))
# mzi_clad(cell,path11, path22, 100, path1_w, path1_l, text="check", layer=layer_wg)

lib.write_gds('TA_check.gds')