# /src/isohypseswallpaper/cli.py
"""
Command-line interface for generating isohypses wallpapers.
"""

import argparse
from isohypseswallpaper import scale, geometry, srtm, wallpaper


def main():
    parser = argparse.ArgumentParser(
        description="Generate a desktop wallpaper from topographic contours."
    )
    parser.add_argument("--lat", type=float, required=True, help="Latitude of the center")
    parser.add_argument("--lon", type=float, required=True, help="Longitude of the center")
    parser.add_argument("--zoom", type=int, required=True, help="Zoom level")
    parser.add_argument("--width", type=int, required=True, help="Screen width in pixels")
    parser.add_argument("--height", type=int, required=True, help="Screen height in pixels")
    parser.add_argument("--contour", type=float, default=None, help="Contour interval in meters")
    parser.add_argument("--bgcolor", type=str, default="#2a2a2a", help="Background color")
    parser.add_argument("--contour-color", type=str, default="white", help="Contour line color")
    parser.add_argument("--output", type=str, required=True, help="Output PNG file path")

    args = parser.parse_args()

    # Compute meters per pixel at the center latitude
    m_per_px = scale.meters_per_pixel(args.lat, args.zoom)

    # Compute bounding box in meters
    width_m = args.width * m_per_px
    height_m = args.height * m_per_px
    lat_min, lat_max, lon_min, lon_max = geometry.bounding_box(
        args.lat, args.lon, width_m, height_m
    )

    # Fetch DEM
    dem_array, dem_meta = srtm.get_dem(
        lat_min, lat_max, lon_min, lon_max, resolution=30
    )

    # Generate wallpaper
    wallpaper.generate_wallpaper(
        dem_array=dem_array,
        lat=args.lat,
        lon=args.lon,
        zoom=args.zoom,
        width=args.width,
        height=args.height,
        contour_interval=args.contour,
        contour_color=args.contour_color,
        background_color=args.bgcolor,
        dem_source="SRTM1",
        dem_resolution=30,
        output_path=args.output,
    )

    print(f"Wallpaper saved to {args.output}")


if __name__ == "__main__":
    main()
