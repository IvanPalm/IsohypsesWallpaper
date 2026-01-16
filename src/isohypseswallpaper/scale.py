"""
Scale utilities.

This module converts between zoom levels, pixel dimensions,
and real-world distances using Web Mercator conventions.
"""

from __future__ import annotations

import math


WEB_MERCATOR_INITIAL_RESOLUTION = 156543.03392804097
"""
Meters per pixel at zoom level 0 at the equator.
Defined by the Web Mercator projection.
"""


def meters_per_pixel(latitude_deg: float, zoom: int) -> float:
    """
    Compute the ground resolution (meters per pixel) at a given latitude
    and zoom level, following Web Mercator conventions.

    Parameters
    ----------
    latitude_deg : float
        Latitude in degrees.
    zoom : int
        Zoom level (non-negative integer).

    Returns
    -------
    float
        Meters per pixel at the given latitude and zoom.
    """
    if zoom < 0:
        raise ValueError("zoom level must be non-negative")

    latitude_rad = math.radians(latitude_deg)
    return WEB_MERCATOR_INITIAL_RESOLUTION * math.cos(latitude_rad) / (2**zoom)


def extent_meters(
    latitude_deg: float,
    zoom: int,
    width_px: int,
    height_px: int,
) -> tuple[float, float]:
    """
    Compute the real-world width and height (in meters) of an image
    at a given latitude, zoom level, and pixel dimensions.

    Parameters
    ----------
    latitude_deg : float
        Latitude in degrees.
    zoom : int
        Zoom level.
    width_px : int
        Image width in pixels.
    height_px : int
        Image height in pixels.

    Returns
    -------
    (float, float)
        Width and height in meters.
    """
    if width_px <= 0 or height_px <= 0:
        raise ValueError("image dimensions must be positive")

    mpp = meters_per_pixel(latitude_deg, zoom)
    return width_px * mpp, height_px * mpp
