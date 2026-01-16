from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
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
    Generate a wallpaper with hillshades over a single-color background.
    """
    # Resample DEM to match target resolution
    zoom_y = height_px / dem.shape[0]
    zoom_x = width_px / dem.shape[1]
    dem_resampled = zoom(dem, (zoom_y, zoom_x), order=1)

    # Compute hillshade
    ls = LightSource(azdeg=315, altdeg=45)
    hillshade = ls.hillshade(dem_resampled, vert_exag=1)

    # Prepare figure
    fig, ax = plt.subplots(figsize=(width_px / 100, height_px / 100), dpi=100)
    ax.set_facecolor(background_color)  # single-color background

    # Overlay hillshade as grayscale
    ax.imshow(hillshade, cmap="gray", origin="upper", extent=(0, width_px, 0, height_px))

    # Draw contours
    if contour_interval is not None:
        levels = np.arange(dem_resampled.min(), dem_resampled.max(), contour_interval)
        ax.contour(dem_resampled, levels=levels, colors=contour_color, linewidths=0.5, origin="upper")

    ax.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)
    plt.close()
