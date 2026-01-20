# src/isohypseswallpaper/wallpaper.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, to_rgb, to_rgba
from scipy.ndimage import zoom
from PIL import Image
from . import metadata, scale, themes

def interpolate_colors(colors: list[str], values: np.ndarray) -> np.ndarray:
    """
    Interpolate RGB colors over a normalized array of values (0-1).

    colors: list of hex colors (e.g. ["#000000", "#ffffff"])
    values: 2D array normalized 0..1
    Returns: 3D array of RGB values
    """
    from matplotlib.colors import to_rgb
    colors_rgb = np.array([to_rgb(c) for c in colors])
    n = len(colors_rgb)
    # Map values 0..1 to index in gradient
    idx = values * (n - 1)
    idx_floor = np.floor(idx).astype(int)
    idx_ceil = np.ceil(idx).astype(int)
    t = idx - idx_floor
    rgb = (1 - t[..., None]) * colors_rgb[idx_floor] + t[..., None] * colors_rgb[idx_ceil]
    return rgb

def generate_wallpaper(
    dem_array: np.ndarray,
    lat: float,
    lon: float,
    zoom_level: int,
    width: int,
    height: int,
    contour_interval: float | None = None,
    background_color: str | list[str] = "#2a2a2a",
    contour_color: str | list[str] = "white",
    theme: str | None = None,
    dem_source: str = "SRTM1",
    dem_resolution: int = 30,
    output_path: str = "wallpaper.png",
) -> None:
    """
    Generate a desktop wallpaper with hillshades, optional contour lines,
    and dynamic/static color themes.

    Parameters
    ----------
    dem_array : np.ndarray
        2D array of elevation values
    lat, lon : float
        Center coordinates
    zoom_level : int
        Zoom level
    width, height : int
        Target image size in pixels
    contour_interval : float | None
        Spacing between contour lines
    background_color : str | list[str]
        Single color or gradient (dynamic) for background
    contour_color : str | list[str]
        Single color or gradient (dynamic) for contours
    theme : str | None
        Optional theme to override colors
    dem_source : str
        Source DEM
    dem_resolution : int
        Resolution in meters
    output_path : str
        Output PNG path
    """
    # --- Apply theme if provided ---
    if theme :
        theme = themes.get_theme(theme)
        background_color = theme["background"]
        contour_color = theme["contour"]

    # --- Resample DEM ---
    zoom_y = height / dem_array.shape[0]
    zoom_x = width / dem_array.shape[1]
    dem_resampled = zoom(dem_array, (zoom_y, zoom_x), order=1)

    # --- Hillshade ---
    ls = LightSource(azdeg=315, altdeg=45)
    hillshade = ls.hillshade(dem_resampled, vert_exag=1)

    # --- Normalize DEM for color mapping ---
    dem_min = np.min(dem_resampled)
    dem_max = np.max(dem_resampled)
    dem_range = dem_max - dem_min + 1e-9
    dem_norm = (dem_resampled - dem_min) / dem_range

    # --- Background ---
    if isinstance(background_color, list):
        bg_rgb = interpolate_colors(background_color, dem_norm)
    else:
        bg_rgb = np.ones((height, width, 3)) * np.array(to_rgb(background_color))

    hillshade_rgb = bg_rgb * hillshade[:, :, np.newaxis]

    # --- Setup matplotlib figure ---
    fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)
    ax.axis("off")
    extent = (0, width, 0, height)
    ax.imshow(hillshade_rgb, origin="upper", extent=extent)

    # --- Contours ---
    if contour_interval is not None:
        levels = np.arange(dem_resampled.min(), dem_resampled.max(), contour_interval)
        if isinstance(contour_color, list):
            n_colors = len(contour_color)
            colors_rgb = [interpolate_colors(contour_color, np.full_like(level, 1.0))[0] for level in levels]
        else:
            colors_rgb = contour_color
        ax.contour(
            dem_resampled,
            levels=levels,
            colors=colors_rgb,
            linewidths=0.5,
            origin="upper",
            extent=extent,
        )

    # --- Tight layout and save image ---
    plt.tight_layout(pad=0)
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)
    plt.close()

    # --- Embed metadata ---
    meters_per_pixel = scale.meters_per_pixel(lat, zoom_level)
    bbox = (
        lat - height * meters_per_pixel / 2,
        lat + height * meters_per_pixel / 2,
        lon - width * meters_per_pixel / 2,
        lon + width * meters_per_pixel / 2,
    )
    exif_dict = metadata.build_exif_metadata(
        version="0.3.0",
        lat=lat,
        lon=lon,
        zoom_level=zoom_level,
        meters_per_pixel=meters_per_pixel,
        width_px=width,
        height_px=height,
        bbox=bbox,
        contour_interval=contour_interval or 0,
        contour_color=str(contour_color),
        background_color=str(background_color),
        dem_source=dem_source,
        dem_resolution=dem_resolution,
    )
    metadata.write_metadata(image_path=output_path, exif_dict=exif_dict, version="0.3.0")
