# Isohypses Wallpaper

Generate minimalist desktop wallpapers from topographic contour lines (isohypses) and hillshaded relief.

The tool fetches SRTM elevation data for a user-defined geographic area and produces a high-resolution image suitable for desktop backgrounds, with customizable colors and contour spacing.

---

## Features

- Generate wallpapers from real-world terrain
- Hillshade relief on a uniform background color
- Optional contour (isohypse) lines
- Configurable via command line
- Uses free SRTM elevation data
- Suitable for widescreen and high-resolution displays

---

## Example Output

- Uniform background color
- Subtle hillshade for depth
- Clean contour lines for structure

![alt text](https://github.com/IvanPalm/IsohypsesWallpaper/blob/main/example_output.png "Example output")

---

## How it works

1. Converts zoom level and latitude to meters-per-pixel using Web Mercator rules
1. Computes a geographic bounding box matching the requested screen size
1. Downloads and clips SRTM elevation data
1. Resamples DEM to match output resolution
1. Computes hillshade
1. Applies hillshade to a uniform background color
1. Saves the final image

---

## Documentation

- [Installation](docs/Installation.md)
- [Usage](docs/Usage.md)
- [Roadmap](docs/Roadmap.md) 

---

## Data Sources

* Elevation data: NASA SRTM (~30m spatial resolution) via [elevation](https://pypi.org/project/elevation/) library

---

## License

GNU General Public License (see [LICENSE](/LICENSE) file).

---

## Acknowledgements

* NASA / USGS for SRTM data
* GDAL and rasterio projects
* matplotlib and scipy communities

