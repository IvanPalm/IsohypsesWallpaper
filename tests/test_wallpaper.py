import numpy as np
import pytest
from unittest.mock import patch

from isohypseswallpaper.wallpaper import generate_wallpaper


@pytest.fixture
def dummy_dem():
    """Create a small dummy DEM array for testing."""
    dem = np.linspace(0, 100, 100).reshape(10, 10)  # 10x10 DEM
    return dem, {}  # Metadata not needed for these tests


@patch.object(generate_wallpaper.__globals__['Image'].Image, "save")
def test_generate_wallpaper_basic(mock_save, dummy_dem):
    """Test that generate_wallpaper runs with hillshade and contours."""
    dem, _ = dummy_dem
    output_path = "dummy_output.png"
    width_px, height_px = 200, 100

    generate_wallpaper(
        dem_array=dem,
        lat=42.0,
        lon=12.0,
        zoom=12,
        width=width_px,
        height=height_px,
        contour_interval=10,
        contour_color="white",
        background_color="#111111",
        output_path=output_path,
    )

    # The function now saves twice: original + metadata embedding
    assert mock_save.call_count == 2
    calls = [call_args[0][0] for call_args in mock_save.call_args_list]
    assert output_path in calls[0]
    assert output_path in calls[1]


@patch.object(generate_wallpaper.__globals__['Image'].Image, "save")
def test_generate_wallpaper_no_contours(mock_save, dummy_dem):
    """Test that wallpaper generates correctly without contours."""
    dem, _ = dummy_dem
    output_path = "dummy_output.png"

    generate_wallpaper(
        dem_array=dem,
        lat=42.0,
        lon=12.0,
        zoom=12,
        width=100,
        height=100,
        contour_interval=None,  # No contours
        contour_color="white",
        background_color="#222222",
        output_path=output_path,
    )

    # The function now saves twice: original + metadata embedding
    assert mock_save.call_count == 2
    calls = [call_args[0][0] for call_args in mock_save.call_args_list]
    assert output_path in calls[0]
    assert output_path in calls[1]
