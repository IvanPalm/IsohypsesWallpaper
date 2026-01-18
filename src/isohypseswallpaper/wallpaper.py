import numpy as np
from PIL import Image
from matplotlib.colors import to_rgb
from scipy.ndimage import zoom as nd_zoom

from . import scale, metadata


def generate_wallpaper(
    dem_array: np.ndarray,
    lat: float,
    lon: float,
    zoom: int,
    width: int,
    height: int,
    contour_interval: float | None,
    contour_color: str = "#FFFFFF",
    background_color: str = "#0E0E0E",
    dem_source: str = "SRTM1",
    dem_resolution: int = 30,
    output_path: str = "wallpaper.png",
) -> None:
    """
    Generate a desktop wallpaper from a digital elevation model (DEM) array,
    optionally overlaying contour lines, and embed EXIF metadata describing
    the generation parameters.

    This function performs the following steps:
    1. Computes the ground resolution (meters per pixel) for the given latitude and zoom.
    2. Scales the DEM array to match the desired output image dimensions.
    3. Normalizes the DEM values and creates a hillshade-like effect.
    4. Generates a uniform RGB background and overlays the hillshade.
    5. Draws contour lines at specified intervals if `contour_interval` is provided.
    6. Converts the result to a PIL Image and saves it to `output_path`.
    7. Builds EXIF metadata describing the wallpaper and embeds it in the PNG.

    Parameters
    ----------
    dem_array : np.ndarray
        2D array of elevation values representing the terrain.
    lat : float
        Latitude of the center of the image (degrees).
    lon : float
        Longitude of the center of the image (degrees).
    zoom : int
        Zoom level used to determine meters per pixel.
    width : int
        Width of the output image in pixels.
    height : int
        Height of the output image in pixels.
    contour_interval : float | None
        Interval between contour lines in meters. If None, no contours are drawn.
    contour_color : str
        Hex color of the contour lines (default: "#FFFFFF").
    background_color : str
        Hex color for the background (default: "#0E0E0E").
    dem_source : str
        Identifier of the DEM source used (default: "SRTM1").
    dem_resolution : int
        Resolution of the DEM in meters (default: 30).
    output_path : str
        Path where the resulting PNG wallpaper will be saved (default: "wallpaper.png").

    Returns
    -------
    None
        Saves the wallpaper image to `output_path` and embeds EXIF metadata.
    """

    # --- Compute meters per pixel at this latitude and zoom ---
    m_per_px = scale.meters_per_pixel(lat, zoom)

    # --- Scale DEM to desired resolution ---
    zoom_y = height / dem_array.shape[0]
    zoom_x = width / dem_array.shape[1]
    dem_resized = nd_zoom(dem_array, (zoom_y, zoom_x))

    # --- Normalize DEM for hillshade effect ---
    norm = (dem_resized - np.min(dem_resized)) / (np.ptp(dem_resized) + 1e-9)

    # --- Create RGB image with uniform background ---
    bg_rgb = np.zeros((height, width, 3), dtype=np.uint8)
    bg_rgb[:, :, :] = np.array(
        [int(255 * x) for x in to_rgb(background_color)], dtype=np.uint8
    )

    # --- Apply hillshade as intensity overlay ---
    gray = (norm * 255).astype(np.uint8)
    for i in range(3):
        bg_rgb[:, :, i] = (
            bg_rgb[:, :, i].astype(np.float32) * 0.5 + gray * 0.5
        ).astype(np.uint8)

    # --- Draw contours ---
    if contour_interval is not None:
        contour_interval_int = int(contour_interval)
        rgb = tuple(int(255 * x) for x in to_rgb(contour_color))
        for level in range(0, int(dem_resized.max()), contour_interval_int):
            mask = np.abs(dem_resized - level) < (contour_interval_int / 10)
            bg_rgb[mask] = rgb

    # --- Convert to PIL Image ---
    img = Image.fromarray(bg_rgb)

    # --- Build metadata ---
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
        contour_interval=contour_interval_int if contour_interval is not None else 0,
        contour_color=contour_color,
        background_color=background_color,
        dem_source=dem_source,
        dem_resolution=dem_resolution,
    )

    # --- Save image first ---
    img.save(output_path)

    # --- Now write metadata ---
    metadata.write_metadata(
        image_path=output_path, exif_dict=exif_dict, version="0.2.0"
    )
