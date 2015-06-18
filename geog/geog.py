import numpy as np
from numpy import arcsin, arctan2, cos, sin, sqrt

r = 6371000.0


def _to_array(*args):
    args = [np.array(a, copy=False) for a in args]
    single = all(a.ndim == 1 for a in args)
    args = np.atleast_2d(*args)

    return single, args


def distance(p0, p1, deg=True):
    single, (p0, p1) = _to_array(p0, p1)
    if deg:
        p0 = np.radians(p0)
        p1 = np.radians(p1)

    lon0, lat0 = p0[:,0], p0[:,1]
    lon1, lat1 = p1[:,0], p1[:,1]

    haversine_dlat = sin((lat1 - lat0) / 2.0) ** 2
    haversine_dlon = sin((lon1 - lon0) / 2.0) ** 2
    a = haversine_dlat + cos(lat0) * cos(lat1) * haversine_dlon
    d = r * 2.0 * arcsin(sqrt(a))

    if single:
        d = d[0]

    return d


def course(p0, p1, deg=True, bearing=False):
    single, (p0, p1) = _to_array(p0, p1)
    if deg:
        p0 = np.radians(p0)
        p1 = np.radians(p1)

    lon0, lat0 = p0[:,0], p0[:,1]
    lon1, lat1 = p1[:,0], p1[:,1]

    dlon = lon1 - lon0
    a = sin(dlon) * cos(lat1)
    b = cos(lat0) * sin(lat1) - sin(lat0) * cos(lat1) * cos(dlon)

    if bearing:
        angle = arctan2(b, a)
    else:
        angle = arctan2(a, b)

    if deg:
        angle = np.degrees(angle)

    if single:
        angle = angle[0]

    return angle
