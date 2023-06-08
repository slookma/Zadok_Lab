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


def r_coupler(path1, path2, radios_turn, path1_seg: list, path1_length: list,
              path2_seg=None, path2_length=None):
    if not isinstance(path1_seg, list):
        raise TypeError("path1_seg must be a list.")

    # Determine the top and bottom paths based on their y-coordinate
    top_path, bot_path = determine_top_bottom_paths(path1, path2)

    # Rotate the top and bottom paths in opposite directions
    rotate_paths(top_path, radios_turn, 'r', 'l')
    rotate_paths(bot_path, radios_turn, 'l', 'r')

    # Change the width of the top and bottom paths
    change_width(top_path, path1_seg, path1_length)
    change_width(bot_path, path2_seg, path2_length, top_path.x)

    # Rotate the top and bottom paths in specific sequence
    rotate_paths(top_path, radios_turn, 'l', 'rr', 'll', 'rr', 'l')
    rotate_paths(bot_path, radios_turn, 'r', 'l', 4 * radios_turn, 'l', 'r')

    # Change the width of the top and bottom paths again
    change_width(top_path, path1_seg, path1_length)
    change_width(bot_path, path2_seg, path2_length, top_path.x)

    # Rotate the top and bottom paths to their final positions
    rotate_paths(top_path, radios_turn, 'l', 'r')
    rotate_paths(bot_path, radios_turn, 'r', 'l')


def determine_top_bottom_paths(path1, path2):
    # Determine which path is on top based on their y-coordinate
    if path1.y > path2.y:
        return path1, path2
    else:
        return path2, path1


def rotate_paths(path, radios_turn, *rotations):
    # Rotate the path by the given rotations
    for rotation in rotations:
        if isinstance(rotation, str):
            path.turn(radios_turn, rotation)
        else:
            path.segment(rotation)


def change_width(path, path_seg, path_length, reference_x=None):
    # Change the width of the path segments based on the given lengths
    if reference_x is None:
        reference_x = path.x

    for i in range(len(path_seg) - 1):
        path.segment(path_length[i]).segment(1, final_width=path_seg[i + 1])

    path.segment(path_seg[-1] if path_seg else reference_x - path.x)


path1_w = [0.1, 3, 0.5, 2, 0.1]
path1_l = [10, 10, 20, 50, 10]
r_coupler(path1, path2, 100, path1_w, path1_l, path1_w, path1_l)
cell.add(path1)
cell.add(path2)

lib.write_gds('TA_gpt.gds')