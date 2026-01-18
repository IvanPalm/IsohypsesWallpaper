from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, to_rgb
from scipy.ndimage import zoom


def generate_wallpaper(
    dem: np.ndarray,
    dem_meta: dict,
    output_path: str,
    width_px: int,
    height_px: int,
    background_color: str = "#2a2a2a",
    contour_color: str = "white",
    contour_interval: float | None = None,
) -> None:
    """
    Generate a wallpaper with hillshades over a single-color background
    and optional contour lines.

    Parameters
    ----------
    dem : np.ndarray
        2D array of elevation values.
    dem_meta : dict
        Metadata (unused here, but kept for API consistency).
    output_path : str
        Path to save the PNG wallpaper.
    width_px : int
        Target image width in pixels.
    height_px : int
        Target image height in pixels.
    background_color : str
        Background color as a matplotlib-compatible color.
    contour_color : str
        Color of contour lines.
    contour_interval : float | None
        Spacing between contour lines (meters). If None, no contours are drawn.
    """
    # Resample DEM to match the target resolution
    zoom_y = height_px / dem.shape[0]
    zoom_x = width_px / dem.shape[1]
    dem_resampled = zoom(dem, (zoom_y, zoom_x), order=1)

    # Compute hillshade
    ls = LightSource(azdeg=315, altdeg=45)
    hillshade = ls.hillshade(dem_resampled, vert_exag=1)

    # Create uniform RGB background and modulate with hillshade
    bg_rgb = np.ones((height_px, width_px, 3))
    bg_rgb[:, :, 0:3] = to_rgb(background_color)
    hillshade_rgb = bg_rgb * hillshade[:, :, np.newaxis]

    # Set up figure
    fig, ax = plt.subplots(figsize=(width_px / 100, height_px / 100), dpi=100)
    ax.axis("off")

    # Define extent so hillshade and contours align perfectly
    extent = (0, width_px, 0, height_px)

    # Plot hillshade over uniform background
    ax.imshow(hillshade_rgb, origin="upper", extent=extent)

    # Overlay contour lines if requested
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

    # Tight layout and save
    plt.tight_layout(pad=0)
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)
    plt.close()
