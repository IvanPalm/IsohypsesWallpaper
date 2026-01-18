import builtins
from argparse import Namespace

import pytest

from isohypseswallpaper import cli


def test_cli_calls_pipeline(monkeypatch):
    """
    Test that the CLI parses arguments correctly and calls the
    main pipeline functions with expected values.
    """

    # --- Mock argparse output ---
    mock_args = Namespace(
        lat=42.0,
        lon=12.0,
        zoom=12,
        width=1920,
        height=1080,
        contour=50.0,
        bgcolor="#1a1a1a",
        contour_color="cyan",
        output="output.png",
    )

    monkeypatch.setattr(cli.argparse.ArgumentParser, "parse_args", lambda self: mock_args)

    # --- Track calls ---
    calls = {}

    def mock_meters_per_pixel(lat, zoom):
        calls["meters_per_pixel"] = (lat, zoom)
        return 10.0

    def mock_bounding_box(lat, lon, width_m, height_m):
        calls["bounding_box"] = (lat, lon, width_m, height_m)
        return 0.0, 1.0, 2.0, 3.0

    def mock_get_dem(lat_min, lat_max, lon_min, lon_max, resolution):
        calls["get_dem"] = (lat_min, lat_max, lon_min, lon_max, resolution)
        return "DEM_ARRAY", {"meta": "data"}

    def mock_generate_wallpaper(**kwargs):
        calls["generate_wallpaper"] = kwargs

    # --- Apply mocks ---
    monkeypatch.setattr(cli.scale, "meters_per_pixel", mock_meters_per_pixel)
    monkeypatch.setattr(cli.geometry, "bounding_box", mock_bounding_box)
    monkeypatch.setattr(cli.srtm, "get_dem", mock_get_dem)
    monkeypatch.setattr(cli.wallpaper, "generate_wallpaper", mock_generate_wallpaper)

    # --- Run CLI ---
    cli.main()

    # --- Assertions ---
    assert calls["meters_per_pixel"] == (42.0, 12)

    width_m_expected = 1920 * 10.0
    height_m_expected = 1080 * 10.0
    assert calls["bounding_box"] == (42.0, 12.0, width_m_expected, height_m_expected)

    assert calls["get_dem"] == (0.0, 1.0, 2.0, 3.0, 30)

    wallpaper_call = calls["generate_wallpaper"]
    assert wallpaper_call["dem_array"] == "DEM_ARRAY"
    assert wallpaper_call["output_path"] == "output.png"
    assert wallpaper_call["width"] == 1920
    assert wallpaper_call["height"] == 1080
    assert wallpaper_call["background_color"] == "#1a1a1a"
    assert wallpaper_call["contour_color"] == "cyan"
    assert wallpaper_call["contour_interval"] == 50.0
