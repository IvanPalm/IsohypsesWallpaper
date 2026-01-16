from affine import Affine
import numpy as np
from unittest.mock import patch, MagicMock

from isohypseswallpaper.srtm import get_dem

def make_dummy_raster(width=10, height=5):
    """Creates a dummy rasterio-like object for testing."""
    dummy = MagicMock()
    dummy.read.return_value = np.ones((height, width), dtype=np.float32)
    dummy.meta = {
        "driver": "GTiff",
        "dtype": "float32",
        "count": 1,
        "crs": "EPSG:4326",
        "transform": Affine.translation(0, 0) * Affine.scale(1, -1),  # basic transform
        "width": width,
        "height": height,
    }
    dummy.transform = dummy.meta["transform"]
    return dummy


@patch("elevation.clip")
@patch("rasterio.open")
def test_get_dem_calls(mock_rasterio_open, mock_elevation_clip):
    """Test that get_dem calls elevation.clip and rasterio.open correctly."""

    # Mock rasterio.open to return dummy raster
    dummy_raster = make_dummy_raster()
    mock_rasterio_open.return_value.__enter__.return_value = dummy_raster

    lat_min, lat_max = 0.0, 1.0
    lon_min, lon_max = 2.0, 3.0

    dem_array, dem_meta = get_dem(lat_min, lat_max, lon_min, lon_max, resolution=30, cache_dir="/tmp/fake")

    # elevation.clip called with correct bounds
    mock_elevation_clip.assert_called_once()
    args, kwargs = mock_elevation_clip.call_args
    assert kwargs["bounds"] == (lon_min, lat_min, lon_max, lat_max)
    assert kwargs["product"] == "SRTM1"
    assert kwargs["output"].endswith("dem.tif")

    # rasterio.open called
    mock_rasterio_open.assert_called_once()

    # Output array matches dummy
    assert np.all(dem_array == 1)
    # Metadata contains height/width keys
    assert dem_meta["height"] == dummy_raster.read.return_value.shape[0]
    assert dem_meta["width"] == dummy_raster.read.return_value.shape[1]
