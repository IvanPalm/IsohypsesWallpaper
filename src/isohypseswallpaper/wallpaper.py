# /src/isohypseswallpaper/wallpaper.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, to_rgb
from scipy.ndimage import zoom as nd_zoom
from PIL import Image, PngImagePlugin
from . import metadata, scale


def generate_wallpaper(
    dem_array: np.ndarray,
    lat: float,
    lon: float,
    zoom: int,
    width: int,
    height: int,
    contour_interval: float | None = None,
    contour_color: str = "white",
    background_color: str = "#2a2a2a",
    dem_source: str = "SRTM1",
    dem_resolution: int = 30,
    output_path: str = "wallpaper.png",
) -> None:
    """
    Generate a desktop wallpaper from a DEM array with v0.1.0 styling:
    hillshade overlay on a uniform background, optional contours, 
    and automatically embed EXIF metadata.

    Parameters
    ----------
    dem_array : np.ndarray
        2D array of elevation values.
    lat : float
        Latitude of the center.
    lon : float
        Longitude of the center.
    zoom : int
        Zoom level.
    width : int
        Width of the output image in pixels.
    height : int
        Height of the output image in pixels.
    contour_interval : float | None
        Interval of contour lines in meters. If None, no contours.
    contour_color : str
        Color of contour lines.
    background_color : str
        Background color as a matplotlib-compatible color.
    dem_source : str
        DEM data source.
    dem_resolution : int
        DEM resolution in meters.
    output_path : str
        File path to save the PNG wallpaper.
    """
    # --- Resample DEM to target resolution ---
    zoom_y = height / dem_array.shape[0]
    zoom_x = width / dem_array.shape[1]
    dem_resampled = nd_zoom(dem_array, (zoom_y, zoom_x), order=1)

    # --- Compute hillshade ---
    ls = LightSource(azdeg=315, altdeg=45)
    hillshade = ls.hillshade(dem_resampled, vert_exag=1)

    # --- Create RGB background modulated by hillshade ---
    bg_rgb = np.ones((height, width, 3))
    bg_rgb[:, :, :] = to_rgb(background_color)
    hillshade_rgb = bg_rgb * hillshade[:, :, np.newaxis]

    # --- Plot with matplotlib ---
    fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)
    ax.axis("off")
    extent = (0, width, 0, height)
    ax.imshow(hillshade_rgb, origin="upper", extent=extent)

    # --- Overlay contours ---
    if contour_interval is not None:
        levels = np.arange(dem_resampled.min(), dem_resampled.max(), contour_interval)
        ax.contour(
            dem_resampled,
            levels=levels,
            colors=contour_color,
            linewidths=0.5,
            origin="upper",
            extent=extent,
        )

    plt.tight_layout(pad=0)
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)
    plt.close(fig)

    # --- Compute meters per pixel for metadata ---
    m_per_px = scale.meters_per_pixel(lat, zoom)

    # --- Build EXIF metadata ---
    exif_dict = metadata.build_exif_metadata(
        version="0.2.0",
        lat=lat,
        lon=lon,
        zoom=zoom,
        meters_per_pixel=m_per_px,
        width_px=width,
        height_px=height,
        bbox=(
            lat - height * m_per_px / 2,
            lat + height * m_per_px / 2,
            lon - width * m_per_px / 2,
            lon + width * m_per_px / 2,
        ),
        contour_interval=int(contour_interval) if contour_interval else 0,
        contour_color=contour_color,
        background_color=background_color,
        dem_source=dem_source,
        dem_resolution=dem_resolution,
    )

    # --- Embed metadata in the PNG ---
    img = Image.open(output_path)
    png_info = PngImagePlugin.PngInfo()
    user_comment = metadata.exif_dict_to_usercomment(exif_dict)
    png_info.add_text("UserComment", user_comment)
    png_info.add_text("Software", "IsohypsesWallpaper")
    img.save(output_path, pnginfo=png_info)
