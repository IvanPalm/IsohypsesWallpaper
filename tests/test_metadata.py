# tests/test_metadata.py

import re
from isohypseswallpaper.metadata import build_exif_metadata, exif_dict_to_usercomment

def test_build_exif_metadata_basic():
    metadata = build_exif_metadata(
        version="0.2.0",
        lat=42.0,
        lon=12.0,
        zoom=12,
        meters_per_pixel=9.554,
        width_px=1920,
        height_px=1080,
        bbox=(41.861448, 42.137605, 11.671616, 12.329808),
        contour_interval=50,
        contour_color="#FFFFFF",
        background_color="#0E0E0E"
    )

    # Basic checks
    assert metadata["IsohypsesWallpaper:Version"] == "0.2.0"
    assert metadata["IsohypsesWallpaper:Generator"] == "isohypseswallpaper"
    assert metadata["IsohypsesWallpaper:Latitude"] == "42.000000"
    assert metadata["IsohypsesWallpaper:Longitude"] == "12.000000"
    assert metadata["IsohypsesWallpaper:BoundingBox"] == "41.861448,42.137605,11.671616,12.329808"


def test_exif_dict_to_usercomment_format():
    metadata = {"A": "1", "B": "2"}
    comment = exif_dict_to_usercomment(metadata)
    lines = comment.splitlines()
    assert len(lines) == 2
    assert "A=1" in lines
    assert "B=2" in lines

def test_generated_at_format():
    metadata = build_exif_metadata(
        version="0.2.0",
        lat=0,
        lon=0,
        zoom=0,
        meters_per_pixel=1.0,
        width_px=1,
        height_px=1,
        bbox=(0, 0, 0, 0),
        contour_interval=1,
        contour_color="#000000",
        background_color="#FFFFFF"
    )
    generated_at = metadata["IsohypsesWallpaper:GeneratedAt"]
    # Check ISO 8601 UTC format
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", generated_at)
