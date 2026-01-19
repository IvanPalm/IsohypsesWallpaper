# /tests/test_geometry.py

import math
import pytest

from isohypseswallpaper.geometry import offset_point, bounding_box
from isohypseswallpaper.scale import meters_per_pixel


def test_offset_point_north_east_consistency():
    """Check that small north/east offsets roughly correspond to expected distances."""
    lat, lon = 0.0, 0.0

    # Offset 1000 m north, 0 m east
    lat1, lon1 = offset_point(lat, lon, 1000, 0)
    # Roughly 0.009 degrees latitude per km near equator
    expected_lat_north = lat + (1000 / 111320)  # approx meters per degree
    assert math.isclose(lat1, expected_lat_north, rel_tol=0.01)
    assert math.isclose(lon1, lon, abs_tol=1e-6)

    # Offset 0 m north, 1000 m east
    lat2, lon2 = offset_point(lat, lon, 0, 1000)
    # Approx meters per degree longitude at equator ~111320
    expected_lon_east = lon + (1000 / 111320)
    assert math.isclose(lat2, lat, abs_tol=1e-6)
    assert math.isclose(lon2, expected_lon_east, rel_tol=0.01)


def test_bounding_box_symmetry():
    """Bounding box should be symmetric around center for small distances."""
    lat_center, lon_center = 10.0, 20.0
    width_m, height_m = 1000, 500

    lat_min, lat_max, lon_min, lon_max = bounding_box(
        lat_center, lon_center, width_m, height_m
    )

    # The center should be roughly midpoint
    center_lat = (lat_min + lat_max) / 2
    center_lon = (lon_min + lon_max) / 2
    assert math.isclose(center_lat, lat_center, abs_tol=1e-6)
    assert math.isclose(center_lon, lon_center, abs_tol=1e-6)

    # Height in meters roughly matches
    north_south_m = (lat_max - lat_min) * 111320  # approximate
    assert math.isclose(north_south_m, height_m, rel_tol=0.05)

    # Width in meters roughly matches at center latitude
    meters_per_deg_lon = 111320 * math.cos(math.radians(lat_center))
    east_west_m = (lon_max - lon_min) * meters_per_deg_lon
    assert math.isclose(east_west_m, width_m, rel_tol=0.05)


def test_bounding_box_negative_dimensions():
    """Bounding box should handle negative width/height by flipping min/max."""
    lat_center, lon_center = 0.0, 0.0
    width_m, height_m = -1000, -500

    lat_min, lat_max, lon_min, lon_max = bounding_box(
        lat_center, lon_center, width_m, height_m
    )

    assert lat_min < lat_max
    assert lon_min < lon_max


def test_offset_zero_returns_same_point():
    """Offset of 0 meters should return original point."""
    lat, lon = 45.0, 12.0
    lat2, lon2 = offset_point(lat, lon, 0, 0)
    assert lat2 == lat
    assert lon2 == lon
