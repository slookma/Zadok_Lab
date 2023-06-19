import gdspy

lib = gdspy.GdsLibrary()
# cells
cell_core = lib.new_cell('core')
cell_clad = lib.new_cell('clad')
cell_finish = lib.new_cell('not')
# layers
layer1 = {"layer": 1, "datatype": 0}
layer2 = {"layer": 2, "datatype": 0}
layer3 = {"layer": 3, "datatype": 0}


def grating(path, dx, start_width, end_width, taper_lenght, num_cycles, cycle_size, fill_part, layer, core=True):
    # taper
    path.segment(taper_lenght, final_width=end_width + dx, **layer).segment(17.5, **layer)
    # create grating
    if core:
        for i in range(num_cycles):
            path.x += fill_part
            path.segment(cycle_size - fill_part, **layer)
    else:
        path.segment(cycle_size * num_cycles, **layer)
    # taper
    path.segment(17.5, **layer).segment(taper_lenght, final_width=start_width + dx, **layer)


path_core = gdspy.Path(0.7)
path_clad = gdspy.Path(0.7+5)

grating(path_core, 0, 0.7, 10, 115, 32+1, 0.600, 0.231, layer1)
grating(path_clad, 5, 0.7, 10, 115, 32+1, 0.600, 0.231, layer2, False)

cell_core.add(path_core)
cell_clad.add(path_clad)

inv = gdspy.boolean(cell_clad, cell_core, 'not', **layer3)
cell_finish.add(inv)

lib.write_gds('grating.gds')
