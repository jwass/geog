import numpy as np
import pytest

import geog

from .common import locs


_p = {
    'bos': {
        30: {
            5000: [-71.00618055,  42.38257097],
            100000: [-69.99732478,  42.8048854]
        },
        60: {
            5000: [-71.02846398999792, 42.39902552366248],
        }
    },
    'dc': {
        30: {
            5000: [-76.96634279,  38.92717236],
            100000: [-76.00921401,  39.35004776],
        },
    },
    'la': {
        30: {
            5000: [-118.20298759,   34.07247409],
            100000: [-117.30499691,   34.49605067],
        },
    },
}


def test_prop_one():
    loc = 'bos'
    a = 30
    d = 5000

    result = geog.propagate(locs[loc], a, d)
    assert len(result) == 2  # If it's a 2d array this will fail
    assert np.allclose(result, _p[loc][a][d])


def test_prop_one_bearing():
    loc = 'bos'
    a = 30
    d = 5000

    result = geog.propagate(locs[loc], a, d, bearing=True)
    assert np.allclose(result, _p[loc][60][d])


def test_prop_n_loc_to_one():
    tlocs = ['bos', 'dc', 'la']
    a = 30
    d = 5000
    expected = [_p[loc][a][d] for loc in tlocs]

    coords = [locs[loc] for loc in tlocs]
    assert np.allclose(geog.propagate(coords, a, d), expected)


def test_prop_n_ang_to_one():
    loc = locs['bos']
    angles = [30, 60]
    d = 5000
    expected = [_p['bos'][ang][d] for ang in angles]

    result = geog.propagate(loc, angles, d)
    assert np.allclose(result, expected)


def test_prop_n_d_to_one():
    loc = locs['bos']
    a = 30
    ds = [5000, 100000]
    expected = [_p['bos'][a][d] for d in ds]

    result = geog.propagate(loc, a, ds)
    assert np.allclose(result, expected)


def test_prop_n_to_n():
    tlocs = ['bos', 'dc', 'la']
    angles = [60, 30, 30]
    ds = [5000, 100000, 5000]

    expected = [_p[loc][a][d] for (loc, a, d) in zip(tlocs, angles, ds)]

    coords = [locs[loc] for loc in tlocs]
    result = geog.propagate(coords, angles, ds)
