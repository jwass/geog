import numpy as np
from numpy import arcsin, arctan2, cos, sin, sqrt

r_earth_mean = 6371000.0

_shape_func = {
    1: np.atleast_1d,
    2: np.atleast_2d,
    3: np.atleast_3d,
}


def _to_arrays(*args):
    nargs = []
    single = True
    for a, ndim in args:
        try:
            arg = np.array(a, copy=False)
        except TypeError:
            # Typically end up in here when list of Shapely geometries is
            # passed in as input.
            arrays = [np.array(el, copy=False) for el in a]
            arg = np.array(arrays, copy=False)
        if arg.ndim != ndim - 1:
            single = False
        arg = _shape_func[ndim](arg)
        nargs.append(arg)

    return single, nargs


def distance(p0, p1, deg=True, r=r_earth_mean):
    single, (p0, p1) = _to_arrays((p0, 2), (p1, 2))
    if deg:
        p0 = np.radians(p0)
        p1 = np.radians(p1)

    lon0, lat0 = p0[:,0], p0[:,1]
    lon1, lat1 = p1[:,0], p1[:,1]

    # h_x used to denote haversine(x): sin^2(x / 2)
    h_dlat = sin((lat1 - lat0) / 2.0) ** 2
    h_dlon = sin((lon1 - lon0) / 2.0) ** 2
    h_angle = h_dlat + cos(lat0) * cos(lat1) * h_dlon
    angle = 2.0 * arcsin(sqrt(h_angle))
    d = r * angle

    if single:
        d = d[0]

    return d


def course(p0, p1, deg=True, bearing=False):
    # http://www.movable-type.co.uk/scripts/latlong.html
    single, (p0, p1) = _to_arrays((p0, 2), (p1, 2))
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


def propagate(p0, angle, d, deg=True, bearing=False, r=r_earth_mean):
    single, (p0, angle, d) = _to_arrays((p0, 2), (angle, 1), (d, 1))
    if not bearing:
        angle = 90 - angle

    angle = np.radians(angle)

    if deg:
        p0 = np.radians(p0)

    lon0, lat0 = p0[:,0], p0[:,1]

    angd = d / r
    lat1 = arcsin(sin(lat0) * cos(angd) + cos(lat0) * sin(angd) * cos(angle))

    a = sin(angle) * sin(angd) * cos(lat0)
    b = cos(angd) - sin(lat0) * sin(lat1)
    lon1 = lon0 + arctan2(a, b)

    p1 = np.column_stack([lon1, lat1])

    if deg:
        p1 = np.degrees(p1)

    if single:
        p1 = p1[0]

    return p1
