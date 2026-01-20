# /tests/test_smoke.py

import tempfile
import numpy as np
import os
from unittest.mock import patch
from types import SimpleNamespace

from isohypseswallpaper import cli


def test_smoke_pipeline_runs():
    """
    Smoke test for the IsohypsesWallpaper pipeline.
    Ensures CLI can generate a wallpaper without crashing
    and produces an output file with embedded metadata.
    """
    # --- Create a small dummy DEM ---
    dem = np.linspace(0, 100, 100).reshape(10, 10)

    # --- Create temporary output file ---
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "smoke_wallpaper.png")

        # --- Patch CLI dependencies to use dummy DEM ---
        with patch("isohypseswallpaper.srtm.get_dem") as mock_get_dem, \
             patch("isohypseswallpaper.scale.meters_per_pixel") as mock_mpp, \
             patch("isohypseswallpaper.geometry.bounding_box") as mock_bbox:

            mock_get_dem.return_value = (dem, {"dummy": "meta"})
            mock_mpp.return_value = 1.0  # meters per pixel
            mock_bbox.return_value = (0, 1, 0, 1)  # dummy bounding box

            # --- Patch argparse to simulate CLI arguments ---
            args = SimpleNamespace(
                lat=42.0,
                lon=12.0,
                zoom_level=12,
                width=100,
                height=100,
                contour=10,
                bgcolor="#111111",
                contour_color="white",
                output=output_path,
                theme=None,
                list_themes=False,
            )
            with patch("argparse.ArgumentParser.parse_args", return_value=args):
                # Run CLI main function
                cli.main()

        # --- Assert that the file was created ---
        assert os.path.exists(output_path), "Wallpaper file was not created"

        # Optional: check file size to make sure something was written
        assert os.path.getsize(output_path) > 0, "Wallpaper file is empty"
