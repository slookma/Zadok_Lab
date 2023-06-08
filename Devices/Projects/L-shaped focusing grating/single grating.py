# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 17:21:18 2023

@author: matan
"""

import numpy
import gdspy


def grating(
    period,
    number_of_teeth,
    fill_frac,
    width,
    position,
    direction,
    lda=1,
    sin_theta=0,
    focus_distance=-1,
    focus_width=-1,
    tolerance=0.001,
    layer=50,
    datatype=0,
):
    """
    Straight or focusing grating.

    period          : grating period
    number_of_teeth : number of teeth in the grating
    fill_frac       : filling fraction of the teeth (w.r.t. the period)
    width           : width of the grating
    position        : grating position (feed point)
    direction       : one of {'+x', '-x', '+y', '-y'}
    lda             : free-space wavelength
    sin_theta       : sine of incidence angle
    focus_distance  : focus distance (negative for straight grating)
    focus_width     : if non-negative, the focusing area is included in
                      the result (usually for negative resists) and this
                      is the width of the waveguide connecting to the
                      grating
    tolerance       : same as in `path.parametric`
    layer           : GDSII layer number
    datatype        : GDSII datatype number

    Return `PolygonSet`
    """
    if focus_distance < 0:
        p = gdspy.L1Path(
            (
                position[0] - 0.5 * width,
                position[1] + 0.5 * (number_of_teeth - 1 + fill_frac) * period,
            ),
            "+x",
            period * fill_frac,
            [width],
            [],
            number_of_teeth,
            period,
            layer=layer,
            datatype=datatype,
        )
    else:
        neff = lda / float(period) + sin_theta
        qmin = int(focus_distance / float(period) + 0.5)
        p = gdspy.Path(period * fill_frac, position)
        c3 = neff ** 2 - sin_theta ** 2
        w = 0.5 * width
        for q in range(qmin, qmin + number_of_teeth):
            c1 = q * lda * sin_theta
            c2 = (q * lda) ** 2
            p.parametric(
                lambda t: (
                    width * t - w,
                    (c1 + neff * numpy.sqrt(c2 - c3 * (width * t - w) ** 2)) / c3,
                ),
                tolerance=tolerance,
                max_points=0,
                layer=layer,
                datatype=datatype,
            )
            p.x = position[0]
            p.y = position[1]
        sz = p.polygons[0].shape[0] // 2
        if focus_width == 0:
            p.polygons[0] = numpy.vstack((p.polygons[0][:sz, :], [position]))
        elif focus_width > 0:
            p.polygons[0] = numpy.vstack(
                (
                    p.polygons[0][:sz, :],
                    [
                        (position[0] + 0.5 * focus_width, position[1]),
                        (position[0] - 0.5 * focus_width, position[1]),
                    ],
                )
            )
        p.fracture()
    if direction == "-x":
        return p.rotate(0.5 * numpy.pi, position)
    elif direction == "+x":
        return p.rotate(-0.5 * numpy.pi, position)
    elif direction == "-y":
        return p.rotate(numpy.pi, position)
    else:
        return p



lib = gdspy.GdsLibrary()
cell = lib.new_cell('HUJI_couplers')

cell.add(grating(            
            0.626,
            28,
            0.5,
            19,
            (0, 0),
            "-y",
            1.55,
            numpy.sin(numpy.pi * 8 / 180),
            21.5,
            0.7,
            tolerance=0.001,
            )
    )




gdspy.LayoutViewer(lib)
lib.write_gds("photonics.gds")

# Enable running on the same kernel
gdspy.current_library = gdspy.GdsLibrary()