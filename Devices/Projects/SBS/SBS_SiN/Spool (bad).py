# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 10:26:45 2026

@author: USER
"""

import gdspy
import numpy as np

# -----------------
# Parameters [um]
# -----------------
wg_width = 0.5
bend_radius = 50
pitch = 8
n_turns = 20
input_length = 200
output_length = 200
layer = 1

gds_name = "long_spool_waveguide.gds"

# -----------------
# Create layout
# -----------------
lib = gdspy.GdsLibrary()
cell = lib.new_cell("SPOOL_WG")

path = gdspy.RobustPath(
    (-input_length, 0),
    wg_width,
    layer=layer,
    datatype=0,
    ends="flush"
)

# Input straight
path.segment((0, 0))

# Archimedean spiral / spool
theta_max = 2 * np.pi * n_turns
n_pts = 3000
theta = np.linspace(0, theta_max, n_pts)

# Radius increases gradually
r = bend_radius + pitch * theta / (2 * np.pi)

x = r * np.cos(theta)
y = r * np.sin(theta)

# Shift spiral so it starts at (0, 0)
x -= x[0]
y -= y[0]

points = np.column_stack((x, y))

# Add spiral points
for p in points[1:]:
    path.segment(tuple(p))

# Output straight
last_point = points[-1]
last_angle = theta[-1]

# Tangent direction at spiral end
dx = -np.sin(last_angle)
dy =  np.cos(last_angle)

out_end = last_point + output_length * np.array([dx, dy])
path.segment(tuple(out_end))

cell.add(path)

# Add markers/text
cell.add(gdspy.Text("Input", 20, (-input_length, -30), layer=10))
cell.add(gdspy.Text("Output", 20, tuple(out_end + np.array([20, 20])), layer=10))



gdspy.LayoutViewer(lib)
gdspy.current_library = gdspy.GdsLibrary()

# Save
# lib.write_gds(gds_name)

# print(f"Saved: {gds_name}")