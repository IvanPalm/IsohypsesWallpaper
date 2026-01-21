# src/isohypseswallpaper/wallpaper.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import (
    LightSource,
    to_rgb,
    LinearSegmentedColormap,
    Normalize,
)
from scipy.ndimage import zoom
from . import metadata, scale, themes


def interpolate_colors(colors: list[str], values: np.ndarray) -> np.ndarray:
    """
    Interpolate RGB colors over a normalized array of values (0-1).

    colors: list of hex colors (e.g. ["#000000", "#ffffff"])
    values: array normalized 0..1
    Returns: array with last dimension RGB
    """
    colors_rgb = np.array([to_rgb(c) for c in colors])
    n = len(colors_rgb)

    idx = values * (n - 1)
    idx_floor = np.floor(idx).astype(int)
    idx_ceil = np.clip(idx_floor + 1, 0, n - 1)
    t = idx - idx_floor

    return (1 - t[..., None]) * colors_rgb[idx_floor] + t[..., None] * colors_rgb[idx_ceil]


def make_colormap(colors: list[str], name: str = "custom"):
    """Create a matplotlib colormap from a list of colors."""
    return LinearSegmentedColormap.from_list(name, colors)


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
    """

    # --- Apply theme ---
    if theme:
        theme_def = themes.get_theme(theme)
        background_color = theme_def["background"]
        contour_color = theme_def["contour"]

    # --- Resample DEM ---
    zoom_y = height / dem_array.shape[0]
    zoom_x = width / dem_array.shape[1]
    dem_resampled = zoom(dem_array, (zoom_y, zoom_x), order=1)

    # --- Hillshade ---
    ls = LightSource(azdeg=315, altdeg=45)
    hillshade = ls.hillshade(dem_resampled, vert_exag=1)

    # --- Normalize DEM ---
    dem_min = dem_resampled.min()
    dem_max = dem_resampled.max()
    dem_norm = (dem_resampled - dem_min) / (dem_max - dem_min + 1e-9)

    # --- Background ---
    if isinstance(background_color, list):
        bg_rgb = interpolate_colors(background_color, dem_norm)
    else:
        bg_rgb = np.ones((height, width, 3)) * np.array(to_rgb(background_color))

    hillshade_rgb = bg_rgb * hillshade[:, :, None]

    # --- Figure ---
    fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)
    ax.axis("off")
    extent = (0, width, 0, height)

    ax.imshow(hillshade_rgb, origin="upper", extent=extent)

    # --- Contours ---
    if contour_interval is not None:
        levels = np.arange(dem_min, dem_max, contour_interval)

        if isinstance(contour_color, list):
            cmap = make_colormap(contour_color, name="contour_gradient")
            norm = Normalize(vmin=dem_min, vmax=dem_max)

            ax.contour(
                dem_resampled,
                levels=levels,
                cmap=cmap,
                norm=norm,
                linewidths=0.6,
                origin="upper",
                extent=extent,
            )
        else:
            ax.contour(
                dem_resampled,
                levels=levels,
                colors=contour_color,
                linewidths=0.6,
                origin="upper",
                extent=extent,
            )

    # --- Save ---
    plt.tight_layout(pad=0)
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)
    plt.close()

    # --- Metadata ---
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

    metadata.write_metadata(
        image_path=output_path,
        exif_dict=exif_dict,
        version="0.3.0",
    )
