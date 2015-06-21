import numpy as np
import pytest

import geog

from .common import locs

_d = {
    'bos': {
        'dc': 632473.67118456389,
        'la': 4170235.3567447257,
    },
    'dc': {
        'bos': 632473.67118456389,
        'la': 3694421.2605172736,
    },
    'la': {
        'bos': 4170235.3567447257,
        'dc': 3694421.2605172736,
    }
}


def test_distance_one():
    result = geog.distance(locs['bos'], locs['la'])
    # Make sure we didn't get back an array
    with pytest.raises(TypeError):
        len(result)

    expected = _d['bos']['la']
    assert np.allclose(result, expected)


def test_distance_n_to_one():
    points = [locs['bos'], locs['dc'], locs['la']]
    result = geog.distance(points, locs['bos'])
    expected = [0.0, _d['dc']['bos'], _d['la']['bos']]

    assert np.allclose(result, expected)


def test_distance_one_to_n():
    points = [locs['bos'], locs['dc'], locs['la']]
    result = geog.distance(locs['bos'], points)
    expected = [0.0, _d['dc']['bos'], _d['la']['bos']]

    assert np.allclose(result, expected)


def test_distance_n_to_n():
    points0 = [locs['bos'], locs['dc'], locs['la']]
    points1 = [locs['dc'], locs['la'], locs['bos']]
    result = geog.distance(points0, points1)
    expected = [_d['bos']['dc'], _d['dc']['la'], _d['la']['bos']]

    assert np.allclose(result, expected)
