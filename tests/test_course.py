import numpy as np
import pytest

import geog

from .common import locs


_c = {
    'bos': {
        'dc': -125.41889675,
        'la': -86.76437003,
    },
    'dc': {
        'bos': 50.69778072,
        'la': -85.35172249,
    },
    'la': {
        'bos': 62.9245438,
        'dc': 69.41192904,
    },
}


def assert_course(p0, p1, expected):
    try:
        len(expected)
        array = True
    except TypeError:
        array = False

    result = geog.course(p0, p1)
    if not array:
        with pytest.raises(TypeError):
            len(result)

    assert np.allclose(result, expected)

    result = geog.course(p0, p1, bearing=True)
    # Constrain between -180 and 180
    bearing = 90 - expected
    bearing = np.where(bearing > 180, bearing - 360, bearing)
    assert np.allclose(result, bearing)


def test_course_one():
    assert_course(locs['bos'], locs['la'], _c['bos']['la'])


def test_course_n_to_one():
    p0 = [locs['bos'], locs['dc']]
    p1 = locs['la']
    expected = np.array([_c['bos']['la'], _c['dc']['la']])
    assert_course(p0, p1, expected)


def test_course_n_to_n():
    p0 = [locs['bos'], locs['dc'], locs['la']]
    p1 = [locs['dc'], locs['la'], locs['bos']]
    expected = np.array([_c['bos']['dc'], _c['dc']['la'], _c['la']['bos']])
    assert_course(p0, p1, expected)
