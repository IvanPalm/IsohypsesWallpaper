from datetime import datetime, timezone
from typing import Tuple, Dict
from PIL import PngImagePlugin, Image

def build_exif_metadata(
    *,
    version: str,
    lat: float,
    lon: float,
    zoom: int,
    meters_per_pixel: float,
    width_px: int,
    height_px: int,
    bbox: Tuple[float, float, float, float],
    contour_interval: int,
    contour_color: str,
    background_color: str,
    dem_source: str = "SRTM1",
    dem_resolution: int = 30,
) -> Dict[str, str]:
    """
    Build a dictionary of EXIF-compatible metadata for IsohypsesWallpaper.
    """
    lat_min, lat_max, lon_min, lon_max = bbox
    metadata = {
        "IsohypsesWallpaper:Version": version,
        "IsohypsesWallpaper:Generator": "isohypseswallpaper",
        "IsohypsesWallpaper:GeneratedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "IsohypsesWallpaper:Latitude": f"{lat:.6f}",
        "IsohypsesWallpaper:Longitude": f"{lon:.6f}",
        "IsohypsesWallpaper:Zoom": str(zoom),
        "IsohypsesWallpaper:MetersPerPixel": f"{meters_per_pixel:.3f}",
        "IsohypsesWallpaper:WidthPx": str(width_px),
        "IsohypsesWallpaper:HeightPx": str(height_px),
        "IsohypsesWallpaper:BoundingBox": f"{lat_min:.6f},{lat_max:.6f},{lon_min:.6f},{lon_max:.6f}",
        "IsohypsesWallpaper:ContourIntervalM": str(contour_interval),
        "IsohypsesWallpaper:ContourColor": contour_color,
        "IsohypsesWallpaper:BackgroundColor": background_color,
        "IsohypsesWallpaper:DEMSource": dem_source,
        "IsohypsesWallpaper:DEMResolutionM": str(dem_resolution),
    }
    return metadata


def exif_dict_to_usercomment(metadata: Dict[str, str]) -> str:
    """
    Convert metadata dictionary to a single string for EXIF UserComment.
    """
    return "\n".join(f"{k}={v}" for k, v in metadata.items())


def write_metadata(
    image_path: str,
    exif_dict: Dict[str, str],
    version: str = "0.2.0"
) -> None:
    """
    Embed metadata into a PNG image at `image_path`.
    """
    img = Image.open(image_path)
    png_info = PngImagePlugin.PngInfo()
    user_comment = exif_dict_to_usercomment(exif_dict)
    png_info.add_text("UserComment", user_comment)
    png_info.add_text("Software", f"IsohypsesWallpaper {version}")
    img.save(image_path, pnginfo=png_info)
