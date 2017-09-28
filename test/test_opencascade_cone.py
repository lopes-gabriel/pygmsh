#! /usr/bin/env python
# -*- coding: utf-8 -*-
from math import pi
import pygmsh
import pytest

from helpers import compute_volume


@pytest.mark.skipif(
    pygmsh.get_gmsh_major_version() < 3,
    reason='requires Gmsh >= 3'
    )
def test():
    geom = pygmsh.opencascade.Geometry(
        characteristic_length_min=0.1,
        characteristic_length_max=0.1,
        )

    geom.add_cone([0.0, 0.0, 0.0], [0.0, 0.0, 1.0], 1.0, 0.3, 1.25*pi)

    ref = 0.90779252263
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('opencascade_cone.vtu', *test())