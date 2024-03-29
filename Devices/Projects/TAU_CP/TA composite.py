"""
code summery:
1. import - GDSpy and numpy
2. gds specifications
3. parameters of the design
4. what to write to GDS - CP, ref1, ref2 -
    specifications when they are writen - a while loop
    at the end of the code
5. functions (logical order):
    a. whole_design - creates the core and the clad by calling create_core_clad
        twice and doing a boolian operation
    b. create_core_clad - creates core are clad - by request.
        calls the grating and composite_mzi to create the couplers and mzi
    c. grating - writes a grating coupler
    d. composite_mzi - calls:
        initialize - to define top/bottom path
        coupler - to create the couplers
        rotate paths - to make the optical distance diffrence
        add text - to write what number coupler we are writing
    e. initialize - defines the top and bottom paths, and makes sure we have a list for the composite section
                raises an error otherwise.
    f. coupler - writes a coupler calls:
        rotate paths - to rotate paths to place
        change widths - to change the width according to the composite needs
    g. rotate paths - nice function that rotates paths as needed
    h. add text - adds a number of text to know what coupler we are using
    i. change widths - a loop that changes the widths according to the design
"""

import gdspy
import numpy

# # gds specifications
# gds starting
lib = gdspy.GdsLibrary()
# layer
layer_wg = {"layer": 174, "datatype": 0}
# cell
cell1 = lib.new_cell('core')
cell2 = lib.new_cell('clad')
cell3 = lib.new_cell('not')

# # parameters
# path1 composite - sections widths and lengths
path1_w = [0.675, 0.665, 0.815]
path1_l = [4.67, 39.75, 13.215]
# path2 composite - sections widths and lengths
path2_w = [0.815, 0.615, 0.655]
path2_l = [4.67, 39.75, 13.215]
# ref1 and ref2 path widths
path1_w_ref = [0.7, 0.7, 0.7]
path1_w_ref_2 = [0.6, 0.6, 0.6]
# turning radios
turning_radios = 50
# coupler specifications
taper_end_width = 10
taper_length = 115
cycle_amount = 32
cycle_period = 0.6
fill_part = 0.28
# path starting point
x = 0
y = 0
counter = 0
offset = [-0.04 + 0.01 * i for i in range(9)]
# # what to write
CP = True
ref_700 = False
ref_700_600 = True


def composite_mzi(cell_top, path1, path2, radios_turn, path1_seg: list, path1_length: list,
                  path2_seg=None, path2_length=None, text=None, core=True, dx=0,
                  layer={"layer": 0, "datatype": 0}):
    # 1. Initialize the paths
    top_path, bot_path = initialize(path1, path2, path1_seg)
    top_path_w = 2*top_path.w
    bot_path_w = 2*bot_path.w
    # 2. Coupler 1
    coupler(top_path, bot_path, radios_turn, path1_seg, path1_length, path2_seg, path2_length, dx, core=core,
            layer=layer)

    # 3. Add text
    add_text(cell_top, top_path, text, layer=layer)

    # 4. Optical distance of paths
    rotate_paths(top_path, radios_turn, [2 * radios_turn], layer=layer)
    rotate_paths(bot_path, radios_turn, ['l', 'r'], layer=layer)
    top_path.segment(1, final_width=top_path_w, **layer)
    bot_path.segment(1, final_width=bot_path_w, **layer)
    rotate_paths(top_path, radios_turn, [2 * radios_turn], layer=layer)
    rotate_paths(bot_path, radios_turn, ['r', 'l'], layer=layer)
    # 5. Coupler 2 (same as Coupler 1)
    coupler(top_path, bot_path, radios_turn, path1_seg, path1_length, path2_seg, path2_length, dx, core=core,
            layer=layer)


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
            path2_seg=None, path2_length=None, dx=0, core=True, layer={"layer": 0, "datatype": 0}):
    # Rotate the top and bottom paths to their final positions
    rotate_paths(top_path, radios_turn, ['r', 'l'], layer=layer)
    rotate_paths(bot_path, radios_turn, ['l', 'r'], layer=layer)

    # Change the width of the top and bottom paths
    change_width(top_path, path1_seg, path1_length, dx, core=core, layer=layer)

    if path2_seg:
        change_width(bot_path, path2_seg, path2_length, dx, layer=layer)
    else:
        bot_path.segment(1, **layer).segment(top_path.x - bot_path.x - 1, **layer). \
            segment(1, **layer)
    if top_path.x != bot_path.x:
        raise TypeError("Wave guides in offset")

    # Rotate the top and bottom paths to their final positions
    rotate_paths(top_path, radios_turn, ['l', 'r'], layer=layer)
    rotate_paths(bot_path, radios_turn, ['r', 'l'], layer=layer)


def add_text(cell, top_path, text, layer={"layer": 0, "datatype": 0}):
    if text:
        labeling = gdspy.Text(text, 40, (top_path.x, top_path.y + 10))
        cell.add(labeling)


def rotate_paths(path, radios_turn, rotations, layer={"layer": 0, "datatype": 0}):
    # Rotate the path
    for rotation in rotations:
        if isinstance(rotation, str):
            path.turn(radios_turn, rotation, **layer)
        else:
            path.segment(rotation, **layer)


def change_width(path, path_seg, path_length, dx=0, core=True, layer={"layer": 0, "datatype": 0}):
    # Add taper at the start
    # if core:
    #     path.segment(1, final_width=0.4+dx, **layer)
    # else:
    #     path.segment(1, **layer)

    # Change the width of the path segments based on the given lengths
    for t in range(len(path_seg)):
        path.segment(1, final_width=path_seg[t] + dx, **layer).segment(path_length[t], **layer)

    # Add taper at the end
    # if core:
    #     path.segment(1, final_width=0.7+dx, **layer)
    # else:
    #     path.segment(1, **layer)


def grating(path, dx, start_width, end_width, taper_length, num_cycles,
            cycle_size, fill_part, layer={"layer": 0, "datatype": 0}, core=True):
    """
    the function gets a path and adds to it a grating coupler
    :param path: the path to add the grating coupler to
    :param dx: the extra size for the classic grating: 0 for core, 5 for clad
    :param start_width: WG size at beginning (and end) of the coupler
    :param end_width: the width of the WG when the couping happens
    :param taper_length: how ling the tapering should be
    :param num_cycles: how many gratings there are
    :param cycle_size: the period of every cycle
    :param fill_part: how much of the cycle should be full
    :param layer: if wanted - what layer should it be added to
    :param core: boolean - if core creates grating, else makes a path for clad
    """

    # taper
    path.segment(taper_length, final_width=end_width + dx, **layer).segment(17.5, **layer)
    # create grating if core
    if core:
        for i in range(num_cycles):
            path.x += fill_part
            path.segment(cycle_size - fill_part, **layer)
    else:  # for clad
        path.segment(cycle_size * num_cycles, **layer)
    # taper
    path.segment(17.5, **layer).segment(taper_length, final_width=start_width + dx, **layer)


def create_core_clad(cell, x, y, turning_radios, coupling_dis, wg_width_1, wg_width_2, taper_end_width, taper_length,
                     cycle_amount, cycle_period, fill_part, composite_width1, composite_length1,
                     composite_width2=None, composite_length2=None, text=None, core=True):
    # create paths
    path1 = gdspy.Path(wg_width_1, (x, y))
    path2 = gdspy.Path(wg_width_2, (x, y - 4 * turning_radios - coupling_dis - (wg_width_1 + wg_width_2) / 2))

    if core:
        dx = 0
    else:
        dx = 5

    # grating couplers "in" for paths
    grating(path1, dx, wg_width_1, taper_end_width, taper_length, cycle_amount, cycle_period, fill_part, core=core)
    grating(path2, dx, wg_width_2, taper_end_width, taper_length, cycle_amount, cycle_period, fill_part, core=core)

    # create MZI
    composite_mzi(cell, path1, path2, turning_radios, composite_width1,
                  composite_length1, composite_width2, composite_length2, text=text, dx=dx, core=core)

    # grating couplers "out" for paths
    grating(path1, dx, wg_width_1, taper_end_width, taper_length, cycle_amount, cycle_period, fill_part, core=core)
    grating(path2, dx, wg_width_2, taper_end_width, taper_length, cycle_amount, cycle_period, fill_part, core=core)

    # return paths
    return path1, path2


def whole_design(cell_core, cell_clad, cell_design, x, y, turning_radios, coupling_dis, wg_width_1, wg_width_2,
                 taper_end_width, taper_length, cycle_amount, cycle_period, fill_part,
                 composite_width1, composite_length1, composite_width2=None, composite_length2=None,
                 text=None):
    # Create core
    path1_core, path2_core = create_core_clad(cell_design, x, y, turning_radios, coupling_dis, wg_width_1, wg_width_2,
                                              taper_end_width,
                                              taper_length, cycle_amount, cycle_period, fill_part,
                                              composite_width1, composite_length1, composite_width2,
                                              composite_length2, text, core=True)
    # Add core paths to cell_core
    cell_core.add(path1_core).add(path2_core)

    # Create clad
    path1_clad, path2_clad = create_core_clad(cell_design, x, y, turning_radios, coupling_dis, wg_width_1, wg_width_1,
                                              taper_end_width,
                                              taper_length, cycle_amount, cycle_period, fill_part,
                                              composite_width1, composite_length1, composite_width2,
                                              composite_length2, core=False)
    # Add clad paths to cell_clad
    cell_clad.add(path1_clad).add(path2_clad)

    # Create design
    inv = gdspy.boolean(cell_clad, cell_core, 'not')
    cell_design.add(inv)

# # design
while CP:
    for i in range(3):
        for j in range(3):
            path1_w_offset = [element + offset[counter] for element in path1_w]
            path2_w_offset = [element + offset[counter] for element in path2_w]
            wg_1_width = 0.675 + offset[counter]
            wg_2_width = 0.815 + offset[counter]
            wg_dis = 1 - ((wg_1_width) / 2 + (wg_2_width) / 2)
            whole_design(cell1, cell2, cell3, x, y,
                         turning_radios, wg_dis, wg_1_width, wg_2_width, taper_end_width, taper_length,
                         cycle_amount, cycle_period, fill_part, path1_w_offset,
                         path1_l, path2_w_offset, path2_l, text=str(counter + 1))
            y = y-600
            counter += 1
        x = 1800 * (i+1)
        y = 0
    CP = False

# # ref
while ref_700:
# parameter changes
    counter = 0
    x = 0
    y = -2000
    for i in range(3):
        for j in range(3):
            path1_w_offset = [element + offset[counter] for element in path1_w_ref]
            path2_w_offset = [element + offset[counter] for element in path1_w_ref]
            wg_1_width = 0.7 + offset[counter]
            wg_2_width = 0.7 + offset[counter]
            wg_dis = 1-((wg_1_width)/2+(wg_2_width)/2)
            whole_design(cell1, cell2, cell3, x, y,
                         turning_radios, wg_dis,wg_1_width, wg_2_width, taper_end_width, taper_length,
                         cycle_amount, cycle_period, fill_part, path1_w_offset,
                         path1_l, path2_w_offset, path2_l, text=str(counter+1))
            y = y - 600
            counter += 1
        y = -2000
        x = 1800 * (i+1)
    ref_700 = False


# # # ref 600 700
while ref_700_600:
    counter = 0
    x = 0
    y = -4000
    for i in range(3):
        for j in range(3):
            path1_w_offset = [element + offset[counter] for element in path1_w_ref_2]
            path2_w_offset = [element + offset[counter] for element in path1_w_ref]
            wg_1_width = 0.6 + offset[counter]
            wg_2_width = 0.7 + offset[counter]
            wg_dis = 1-(wg_1_width / 2 + wg_2_width / 2)
            whole_design(cell1, cell2, cell3, x, y,
                         turning_radios, wg_dis,wg_1_width, wg_2_width, taper_end_width, taper_length,
                         cycle_amount, cycle_period, fill_part, path1_w_offset,
                         path1_l, path2_w_offset, path2_l, text=str(counter+1))
            y = y - 600
            counter += 1
        y = -4000
        x = 1800 * (i+1)
    ref_700_600 = False

lib.write_gds('TA_check.gds')
