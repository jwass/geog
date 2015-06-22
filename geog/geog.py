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
    """
    Return the distance between two points on the surface of the Earth.

    Parameters
    ----------
    p0 : point-like (or array of point-like) [longitude, latitude] objects
    p1 : point-like (or array of point-like) [longitude, latitude] objects
    deg : bool, optional (default True)
        indicates if p0 and p1 are specified in degrees 
    r : float, optional (default r_earth_mean)
        radius of the sphere 

    Returns
    -------
    d : float

    Reference
    ---------
    http://www.movable-type.co.uk/scripts/latlong.html - Distance

    Note: Spherical earth model. By default uses radius of 6371.0 km.

    """
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
    """
    Compute the initial bearing along the great circle from p0 to p1

    NB: The angle returned by course() is not the traditional definition of
    bearing. It is definted such that 0 degrees to due East increasing
    counter-clockwise such that 90 degrees is due North. To obtain the bearing
    (0 degrees is due North increasing clockwise so that 90 degrees is due
    East), set the bearing flag input to True.

    Parameters
    ----------
    p0 : point-like (or array of point-like) [lon, lat] objects
    p1 : point-like (or array of point-like) [lon, lat] objects
    deg : bool, optional (default True)
        indicates if p0 and p1 are specified in degrees. The returned
        angle is returned in the same units as the input.
    bearing : bool, optional (default False)
        If True, use the classical definition of bearing where 0 degrees is
        due North increasing clockwise so that and 90 degrees is due East.

    Reference
    ---------
    http://www.movable-type.co.uk/scripts/latlong.html - Bearing

    """
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
        angle = arctan2(a, b)
    else:
        angle = arctan2(b, a)

    if deg:
        angle = np.degrees(angle)

    if single:
        angle = angle[0]

    return angle


def propagate(p0, angle, d, deg=True, bearing=False, r=r_earth_mean):
    """
    Given an initial point and angle, move distance d along the surface

    Parameters
    ----------
    p0 : point-like (or array of point-like) [lon, lat] objects
    angle : float (or array of float)
        bearing. Note that by default, 0 degrees is due East increasing 
        clockwise so that 90 degrees is due North. See the bearing flag
        to change the meaning of this angle
    d : float (or array of float)
        distance to move. The units of d should be consistent with input r
    deg : bool, optional (default True)
        Whether both p0 and angle are specified in degrees. The output
        points will also match the value of this flag.
    bearing : bool, optional (default False)
        Indicates whether to interpret the input angle as the classical
        definition of bearing.
    r : float, optional (default r_earth_mean)
        radius of the sphere


    Reference
    ---------
    http://www.movable-type.co.uk/scripts/latlong.html - Destination

    Note: Spherical earth model. By default uses radius of 6371.0 km.

    """
    single, (p0, angle, d) = _to_arrays((p0, 2), (angle, 1), (d, 1))
    if deg:
        p0 = np.radians(p0)
        angle = np.radians(angle)

    if not bearing:
        angle = np.pi / 2.0 - angle

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
