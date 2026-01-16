"""
Geometry utilities.

Compute bounding boxes, offsets, and distances using geodesic calculations.
"""

from __future__ import annotations

from pyproj import Geod

# WGS84 ellipsoid
GEOD = Geod(ellps="WGS84")


def offset_point(
    lat: float,
    lon: float,
    north_m: float,
    east_m: float,
) -> tuple[float, float]:
    """
    Returns a new latitude and longitude offset from the original point
    by north_m meters and east_m meters.
    """
    # Geod.fwd expects azimuth in degrees, distance in meters
    # North offset: azimuth=0 (north)
    # East offset: azimuth=90 (east)
    lon1, lat1, _ = GEOD.fwd(lon, lat, 0, north_m)
    lon2, lat2, _ = GEOD.fwd(lon1, lat1, 90, east_m)
    return lat2, lon2


def bounding_box(
    lat_center: float,
    lon_center: float,
    width_m: float,
    height_m: float,
) -> tuple[float, float, float, float]:
    """
    Returns (lat_min, lat_max, lon_min, lon_max) for a rectangle
    centered at lat_center/lon_center with given width/height in meters.
    """
    half_width = abs(width_m) / 2
    half_height = abs(height_m) / 2

    # Top-right corner
    lat_max, lon_max = offset_point(lat_center, lon_center, half_height, half_width)
    # Bottom-left corner
    lat_min, lon_min = offset_point(lat_center, lon_center, -half_height, -half_width)

    return lat_min, lat_max, lon_min, lon_max
