geog
====

A pure numpy implementation of some geodesic functions. The interfaces intend
to be vectorized according to numpy broadcasting rules compatible with a
variety of inputs including lists, numpy arrays, and Shapely geometries.

Getting Started
---------------

Compute the distance in meters between two locations
```
>>> import geog

>>> boston = [-71.0589, 42.3601]
>>> la = [-118.2500, 34.0500]
>>> dc = [-77.0164, 38.9047]

>>> geog.distance(boston, la)
4179393.4717019284

```

`geog` allows different sizes of inputs conforming to numpy broadcasting
rules
```
>>> paris = [2.3508, 48.8567]
>>> geog.distance([boston, la, dc], paris)



Installation
-----------
geog is hosted on PyPI.

```
pip install geog
```


See also
--------

- [TurfJS](https://www.turfjs.org)
- [Shapely](https://github.com/toblerity/shapely)
- [Proj.4](https://trac.osgeo.org/proj/)
