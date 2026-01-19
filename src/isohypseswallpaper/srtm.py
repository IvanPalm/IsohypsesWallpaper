# /src/isohypseswallpaper/srtm.py

"""
SRTM utilities.

Download, merge, and clip SRTM DEM tiles for a given bounding box.
"""

from __future__ import annotations

import os
import tempfile
import numpy as np
import rasterio
from rasterio.merge import merge
from rasterio.windows import from_bounds
import elevation


def get_dem(
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
    resolution: int = 30,
    cache_dir: str | None = None,
) -> tuple[np.ndarray, dict]:
    """
    Fetch SRTM DEM data for the given bounding box.

    Parameters
    ----------
    lat_min, lat_max, lon_min, lon_max : float
        Geographic bounding box in degrees.
    resolution : int
        Target resolution in meters (default 30m).
    cache_dir : str | None
        Optional directory to cache downloaded tiles.

    Returns
    -------
    tuple
        (DEM array as numpy.ndarray, rasterio metadata dict)
    """
    # Determine cache location
    if cache_dir is None:
        cache_dir = os.path.join(tempfile.gettempdir(), "isohypseswallpaper_srtm")
    os.makedirs(cache_dir, exist_ok=True)

    # Temporary output file path
    dem_file = os.path.join(cache_dir, "dem.tif")

    # Use elevation CLI wrapper to fetch and clip SRTM
    elevation.clip(bounds=(lon_min, lat_min, lon_max, lat_max),
                    output=dem_file,
                    product="SRTM1",
                    cache_dir=cache_dir)

    # Open clipped DEM with rasterio
    with rasterio.open(dem_file) as src:
        window = from_bounds(lon_min, lat_min, lon_max, lat_max, src.transform)
        dem_array = src.read(1, window=window)
        dem_meta = src.meta.copy()
        dem_meta.update({
            "height": dem_array.shape[0],
            "width": dem_array.shape[1],
            "transform": rasterio.windows.transform(window, src.transform),
        })

    return dem_array, dem_meta
