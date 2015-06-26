geog
====

A pure numpy implementation for geodesic functions. The interfaces are
vectorized according to numpy broadcasting rules compatible with a variety of
inputs including lists, numpy arrays, and
[Shapely](http://toblerity.org/shapely/) geometries - allowing for 1-to-1,
N-to-1, or the element-wise N-to-N calculations in a single call.

`geog` uses a spherical Earth model (subject to change) with radius 6371 km.


Operations
---------
`distance` - Compute the distance between any number of points
`course` - Compute the forward azimuth between points (see below for
coordinate system definition)
`propagate` - Starting from points and pointing azimuths, move some
distance and compute the final points.


Getting Started
---------------

Compute the distance in meters between two locations on the surface of the
Earth.
```
>>> import geog

>>> boston = [-71.0589, 42.3601]
>>> la = [-118.2500, 34.0500]

>>> geog.distance(boston, la)
4179393.4717019284


>>> geog.course(boston, la)
-86.764370028262007

```

`geog` allows different sizes of inputs conforming to numpy broadcasting
rules

Compute the distances from several points to one point.
```
>>> dc = [-77.0164, 38.9047]
>>> paris = [2.3508, 48.8567]
>>> geog.distance([boston, la, dc], paris)
array([ 5531131.56144631,  9085960.07227854,  6163490.48394848])

```

Compute the element-wise distance of several points to several points
```
>>> sydney = [151.2094, -33.865]
>>> barcelona = [2.1833, 41.3833]
>>> p_from = [boston, la, dc]
>>> p_to = [paris, sydney, barcelona]
>>> geog.distance(p_from, p_to)
array([  5531131.56144631,  12072666.9425518 ,   6489222.58111716])

```

`geog` functions can take numpy arrays as inputs
```
>>> import numpy as np
>>> points = np.array([boston, la, dc])
>>> points
array([[ -71.0589,   42.3601],
       [-118.25  ,   34.05  ],
       [ -77.0164,   38.9047]])
>>> geog.distance(points, sydney)
array([ 16239763.03982447,  12072666.9425518 ,  15711932.63508411])
```


`geog` functions can also take Shapely geometries as inputs
```
>>> import shapely.geometry
>>> p = shapely.geometry.Point([-90.0667, 29.9500])
>>> geog.distance(points, p)
array([ 2185738.94680724,  2687705.07260978,  1554066.84579387])

```


Other Operations
----------------
Use `propagate` to buffer a single point by passing in multiple angles.

```
>>> n_points = 6
>>> d = 100  # meters
>>> angles = np.linspace(0, 360, n_points)
>>> polygon = geog.propagate(p, angles, d)

```

Compute the length of a line over the surface.
```
>>> np.sum(geog.distance(line[:-1,:], line[1:,:]))
```


Quick Documentation
-------------
`distance(p0, p1, deg=True)`
`course(p0, p1, deg=True, bearing=False)`
`propagate(p0, angle, d, deg=True, bearing=False)`

For all of the above, `p0` or `p1` can be:
- single list, tuple, or Shapely Point of [lon, lat] coordinates
- list of [lon, lat] coordinates or Shapely Points
- N x 2 numpy array of (lon, lat) coordinates

If argument `deg` is False, then all angle arguments, coordinates and
azimuths, will be used as radians. If `deg` is False in `course()`, then it's
output will also be radians.

Consult the documentation on each function for more detailed descriptions of
the arguments.


Conventions
-----------
* All points, or point-like objects assume a longitude, latitude ordering.
* Arrays of points have shape `N x 2`.
* Azimuth/course is measured with 0 degrees as due East, increasing
  counter-clockwise so that 90 degrees is due North. The functions that
operate on azimuth accept a `bearing=True` argument to use the more
traditional definition where 0 degrees is due North increasing clockwise such
that that 90 degrees is due East.


Installation
-----------
geog is hosted on PyPI.

```
pip install geog
```


See also
--------
- `geog` is partly inspired by [TurfJS](https://www.turfjs.org)

- [Shapely](https://github.com/toblerity/shapely)
- [Proj.4](https://trac.osgeo.org/proj/)
