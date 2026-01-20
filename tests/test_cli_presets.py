from argparse import Namespace

import pytest

from isohypseswallpaper import cli
from isohypseswallpaper.presets import SCREEN_PRESETS


def test_cli_uses_1080p_preset(monkeypatch):
    """
    CLI should use the 1080p preset and ignore explicit width/height.
    """

    mock_args = Namespace(
        lat=42.0,
        lon=12.0,
        zoom=12,
        preset="1080p",
        width=999,   # should be ignored
        height=999,  # should be ignored
        contour=20,
        bgcolor="#1a1a1a",
        contour_color="cyan",
        output="output.png",
    )

    monkeypatch.setattr(
        cli.argparse.ArgumentParser,
        "parse_args",
        lambda self: mock_args,
    )

    calls = {}

    monkeypatch.setattr(cli.scale, "meters_per_pixel", lambda lat, zoom: 10.0)
    monkeypatch.setattr(
        cli.geometry,
        "bounding_box",
        lambda lat, lon, w, h: (0, 1, 2, 3),
    )
    monkeypatch.setattr(
        cli.srtm,
        "get_dem",
        lambda *args, **kwargs: ("DEM", {}),
    )

    def mock_generate_wallpaper(**kwargs):
        calls["generate_wallpaper"] = kwargs

    monkeypatch.setattr(cli.wallpaper, "generate_wallpaper", mock_generate_wallpaper)

    cli.main()

    width, height = SCREEN_PRESETS["1080p"]

    assert calls["generate_wallpaper"]["width"] == width
    assert calls["generate_wallpaper"]["height"] == height


def test_cli_custom_resolution_without_preset(monkeypatch):
    """
    CLI should accept width/height when no preset is provided.
    """

    mock_args = Namespace(
        lat=42.0,
        lon=12.0,
        zoom=12,
        preset=None,
        width=1600,
        height=900,
        contour=None,
        bgcolor="#2a2a2a",
        contour_color="white",
        output="output.png",
    )

    monkeypatch.setattr(
        cli.argparse.ArgumentParser,
        "parse_args",
        lambda self: mock_args,
    )

    calls = {}

    monkeypatch.setattr(cli.scale, "meters_per_pixel", lambda lat, zoom: 5.0)
    monkeypatch.setattr(
        cli.geometry,
        "bounding_box",
        lambda lat, lon, w, h: (0, 1, 2, 3),
    )
    monkeypatch.setattr(
        cli.srtm,
        "get_dem",
        lambda *args, **kwargs: ("DEM", {}),
    )

    def mock_generate_wallpaper(**kwargs):
        calls["generate_wallpaper"] = kwargs

    monkeypatch.setattr(cli.wallpaper, "generate_wallpaper", mock_generate_wallpaper)

    cli.main()

    assert calls["generate_wallpaper"]["width"] == 1600
    assert calls["generate_wallpaper"]["height"] == 900


def test_cli_errors_without_preset_or_resolution(monkeypatch):
    """
    CLI should error if neither preset nor width/height are provided.
    """

    mock_args = Namespace(
        lat=42.0,
        lon=12.0,
        zoom=12,
        preset=None,
        width=None,
        height=None,
        contour=None,
        bgcolor="#2a2a2a",
        contour_color="white",
        output="output.png",
    )

    monkeypatch.setattr(
        cli.argparse.ArgumentParser,
        "parse_args",
        lambda self: mock_args,
    )

    with pytest.raises(SystemExit):
        cli.main()
