# /tests/test_scale.py

import math
import pytest

from isohypseswallpaper.scale import (
    meters_per_pixel,
    extent_meters,
    WEB_MERCATOR_INITIAL_RESOLUTION,
)


def test_meters_per_pixel_at_equator_zoom_0():
    """At the equator and zoom 0, resolution should match the constant."""
    mpp = meters_per_pixel(latitude_deg=0.0, zoom=0)
    assert math.isclose(
        mpp,
        WEB_MERCATOR_INITIAL_RESOLUTION,
        rel_tol=1e-9,
    )


def test_meters_per_pixel_halves_each_zoom_level():
    """Each increment in zoom level halves the meters per pixel."""
    lat = 0.0
    mpp_z10 = meters_per_pixel(lat, zoom=10)
    mpp_z11 = meters_per_pixel(lat, zoom=11)

    assert math.isclose(mpp_z11, mpp_z10 / 2, rel_tol=1e-9)


def test_meters_per_pixel_decreases_with_latitude():
    """Resolution should decrease as latitude increases."""
    mpp_equator = meters_per_pixel(0.0, zoom=10)
    mpp_mid_lat = meters_per_pixel(45.0, zoom=10)
    mpp_high_lat = meters_per_pixel(80.0, zoom=10)

    assert mpp_equator > mpp_mid_lat > mpp_high_lat


def test_negative_zoom_raises():
    """Negative zoom levels are invalid."""
    with pytest.raises(ValueError):
        meters_per_pixel(latitude_deg=0.0, zoom=-1)


def test_extent_meters_simple_case():
    """Extent should scale linearly with pixel dimensions."""
    lat = 0.0
    zoom = 10
    width_px = 1920
    height_px = 1080

    width_m, height_m = extent_meters(
        latitude_deg=lat,
        zoom=zoom,
        width_px=width_px,
        height_px=height_px,
    )

    mpp = meters_per_pixel(lat, zoom)

    assert math.isclose(width_m, width_px * mpp, rel_tol=1e-9)
    assert math.isclose(height_m, height_px * mpp, rel_tol=1e-9)


def test_extent_invalid_dimensions():
    """Image dimensions must be positive."""
    with pytest.raises(ValueError):
        extent_meters(0.0, 10, 0, 1080)

    with pytest.raises(ValueError):
        extent_meters(0.0, 10, 1920, -1)
