import numpy as np
import gdspy

# ---------------- Helper: grating creation ----------------
def create_grating_path(cell, priodicity, fill_factor, grating_period, center, radius, angle, WG_WIDTH,
                        direction, LAYER_WG={"layer": 174, "datatype": 0}):
    """
    Creates circular grating rings and returns a gdspy.Path that continues from the slice.
    """
    priodicity = priodicity[0]
    inner_radius = radius - priodicity * fill_factor
    initial_angle = (1 - angle) * np.pi
    final_angle = (1 + angle) * np.pi
    slice_idx = 2 if direction else 0

    # draw concentric grating arcs (filled)
    for _ in range(grating_period):
        arc = gdspy.Round(center, radius, inner_radius=inner_radius,
                          initial_angle=initial_angle, final_angle=final_angle,
                          tolerance=0.0001, **LAYER_WG)
        arc = arc.rotate(direction * np.pi, center)
        cell.add(arc)
        radius -= priodicity
        inner_radius -= priodicity

    # last arc used to slice a waveguide opening and continue with a path
    arc = gdspy.Round(center, radius, initial_angle=initial_angle,
                      final_angle=final_angle, tolerance=0.0001, **LAYER_WG).rotate(direction*np.pi, center)

    # slice the arc to get a 'gap' for the waveguide and create the path start
    x_left = center[0] - WG_WIDTH / (2*np.tan(initial_angle))
    x_right = center[0] + WG_WIDTH / (2*np.tan(initial_angle))
    arc_slice = gdspy.slice(arc, [x_left, x_right], axis=0)

    # create a path that starts at the opening of the slice
    start_x = center[0] + WG_WIDTH / (2*np.tan(initial_angle))
    waveguide_path = gdspy.Path(WG_WIDTH, (start_x, center[1]))

    # add the chosen slice polygon and the path to the cell
    cell.add(arc_slice[slice_idx])
    cell.add(waveguide_path)

    return waveguide_path


# ---------------- Helper: smooth S-bend for path ----------------
def sbend(wgsbend, L, H, layer_1):
    """
    Parametric cosine-shaped S-bend.
    wgsbend: gdspy.Path object already created
    L: total length (x direction)
    H: total offset (y)
    layer_1: dict with keys "layer" and "datatype" or similar
    """
    def sbend_shape(t):
        y = H / 2 * (1 - np.cos(t * np.pi))
        x = L * t
        return (x, y)

    def dtsbend(t):
        dy_dt = H / 2 * np.pi * np.sin(t * np.pi)
        dx_dt = L
        return (dx_dt, dy_dt)


    # Attach parametric segment to the path (number_of_evaluations can be adjusted)
    wgsbend.parametric(sbend_shape, dtsbend, number_of_evaluations=120,
                       layer=layer_1.get("layer", None), datatype=layer_1.get("datatype", None))
    return wgsbend


# -------------------------- PARAMETERS --------------------------
# geometry
WG_WIDTH     = 2.1       # µm
RING_RADIUS  = 300.0     # µm (used for centerline of the ring when drawing)
GAP          = 1.1       # µm (bus-to-ring gap)
BUS_LENGTH   = 1200.0    # µm (straight section of the bus)
LEAD_IN      = 300.0     # µm
LEAD_OUT     = 300.0     # µm
WG_length    = BUS_LENGTH  # keep naming consistent with your old code
racetrack_length=1000
# grating parameters (kept so create_grating_path works)
period = [0.96]
fill_frac = 0.4
teeth = 90
angle = 0.1
direction = 0

# layers
LAYER_WG = {"layer": 101, "datatype": 0}
LAYER_NEG = {"layer": 301, "datatype": 0}
negative = False       # whether to add simple trench shapes (kept from your code)
trench = 3 * WG_WIDTH

# -------------------------- CREATE LIB/CELL --------------------------
lib = gdspy.GdsLibrary()
cell = lib.new_cell("SINGLE_RING_WITH_GRATINGS")

# -------------------------- BUILD DEVICE --------------------------
# center for input grating
center_input = (0.0, 0.0)

# create input grating and obtain the outgoing waveguide path
path1 = create_grating_path(cell, period, fill_frac, teeth, center_input, RING_RADIUS, angle, WG_WIDTH,
                            direction, LAYER_WG=LAYER_WG)

# extend path1 as in your layout
path1.segment(0.1 * WG_length, **LAYER_WG)
sbend(path1, 500, 100, LAYER_WG)
path1.segment(0.05 * WG_length, **LAYER_WG)

# build the ring (side-coupled to the bus). place ring so that its centerline is GAP away
# path1.x and path1.y are the current path end coordinates
ring_init_x = path1.x  # current end x
ring_init_y = path1.y + WG_WIDTH + GAP  # place ring above the bus by WG_WIDTH+GAP

# draw ring as a circular turn (2*pi)
path2 = gdspy.Path(WG_WIDTH, initial_point=(ring_init_x + RING_RADIUS, ring_init_y))
path2.turn(RING_RADIUS, 0.5 * np.pi, **LAYER_WG).segment(racetrack_length,**LAYER_WG)
path2.turn(RING_RADIUS,  np.pi, **LAYER_WG).segment(racetrack_length,**LAYER_WG).turn(RING_RADIUS,  np.pi, **LAYER_WG)
# finish bus after the coupling region
path1.segment(0.65 * WG_length, **LAYER_WG)

# add paths to cell explicitly
cell.add(path1)
cell.add(path2)

# create output grating (aligned with path1 end)
output_center = (path1.x + WG_WIDTH / (2 * np.tan((1 - angle) * np.pi)), path1.y)
create_grating_path(cell, period, fill_frac, teeth, output_center, RING_RADIUS, angle, WG_WIDTH, 1, LAYER_WG=LAYER_WG)

# optional trenches / negative mask (kept simple and similar to your earlier code)
if negative:
    initial_angle = (1 - angle) * np.pi
    final_angle = (1 + angle) * np.pi
    # big arc used as negative/trench example
    arc = gdspy.Round((center_input[0] + trench / np.sin(angle * np.pi), center_input[1]),
                      RING_RADIUS + trench + trench / np.sin(angle * np.pi),
                      initial_angle=initial_angle, final_angle=final_angle,
                      tolerance=0.0001, **LAYER_NEG).rotate(direction * np.pi, center_input)

    path_trench = gdspy.Path(WG_WIDTH + trench * 2, (center_input[0] - 3.23, center_input[1]))
    path_trench.segment(0.1 * WG_length, '+x', **LAYER_NEG)
    sbend(path_trench, 500, 100, LAYER_NEG)
    path_trench.segment(0.2 * WG_length, '+x', **LAYER_NEG)

    path2_trench = gdspy.Path(width=WG_WIDTH + trench * 2,
                              initial_point=(path_trench.x, path_trench.y + WG_WIDTH + GAP))
    path2_trench.turn(300, 2 * np.pi, **LAYER_NEG)
    path_trench.segment(0.7 * WG_length, '+x', **LAYER_NEG)

    arc2 = gdspy.copy(arc)
    arc2.translate(WG_length + 500, 100)
    arc2.rotate(np.pi, (path1.x, path1.y))

    cell.add([arc, path_trench, arc2, path2_trench])

# -------------------------- EXPORT --------------------------
out_name = "single_ring.gds"
lib.write_gds(out_name)
print(f"✅ GDS written to '{out_name}'. Cell name: {cell.name}")
print("Cell polygons (approx):", len(cell.polygons))
# Reset current library so reruns overwrite cleanly
gdspy.current_library = gdspy.GdsLibrary