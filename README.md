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

(Example images can be added here later.)

---

## Installation

### Requirements

- Python 3.12+
- GDAL (required by SRTM/elevation tools)

On Linux (Debian/Ubuntu):

```bash
sudo apt install gdal-bin libgdal-dev
```

On macOS (Homebrew):

```bash
brew install gdal
```

---

### Install with Poetry (development)

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/isohypseswallpaper.git
cd isohypseswallpaper
poetry install
```

---

## Usage

After installation, the CLI tool is available as:

```bash
isohypses-wallpaper
```

### Basic example

```bash
isohypses-wallpaper \
  --lat 42.0 \
  --lon 12.0 \
  --zoom 12 \
  --width 1920 \
  --height 1080 \
  --contour 50 \
  --output my_wallpaper.png
```

---

## Command-line options

| Argument          | Description                           |
| ----------------- | ------------------------------------- |
| `--lat`           | Latitude of the map center            |
| `--lon`           | Longitude of the map center           |
| `--zoom`          | Web Mercator zoom level               |
| `--width`         | Output image width in pixels          |
| `--height`        | Output image height in pixels         |
| `--contour`       | Contour interval in meters (optional) |
| `--bgcolor`       | Background color (default: `#2a2a2a`) |
| `--contour-color` | Contour line color (default: `white`) |
| `--output`        | Output image file path                |

> [!TIP]
> Zoom levels follow the standard Web Mercator convention.  
> 
> Lower zoom levels cover larger areas with less detail, higher zoom levels cover smaller areas with more detail.
> 
> Typical usage ranges:
> 
> * Zoom 7–9: large regions, mountain ranges
> * Zoom 10–11: cities and surrounding terrain
> * Zoom 12–13: valleys, ridges, local landscapes
> 
> Very high zoom levels may exceed the native resolution of SRTM data and will not add real terrain detail.

---

## How it works

1. Converts zoom level and latitude to meters-per-pixel using Web Mercator rules
2. Computes a geographic bounding box matching the requested screen size
3. Downloads and clips SRTM elevation data
4. Resamples DEM to match output resolution
5. Computes hillshade
6. Applies hillshade to a uniform background color
7. Optionally overlays contour lines
8. Saves the final image

---

## Design Philosophy

* Minimalist aesthetics
* Accurate geographic proportions
* No map labels, borders, or clutter
* Wallpaper-first (not cartography-first)

---

## Development

### Run tests

```bash
poetry run pytest
```

### Project structure

```text

isohypseswallpaper/  
├── pyproject.toml  
├── README.md  
├── LICENSE  
├── .gitignore  
│  
├── src/  
│   └── isohypseswallpaper/  
│       ├── __init__.py  
│       ├── cli.py          # Command-line interface  
│       ├── scale.py        # Zoom <--> meters conversion  
│       ├── geometry.py     # Bounding box calculations  
│       ├── srtm.py         # DEM fetching and clipping  
│       └── wallpaper.py    # Rendering logic  
│  
└── tests/  
    ├── __init__.py  
    ├── test_cli.py         # CLI integration tests (mocked)  
    ├── test_scale.py       # Tests for zoom / scale utilities  
    ├── test_geometry.py    # Tests for bounding box logic  
    ├── test_srtm.py        # Tests for DEM fetching (mocked I/O)  
    └── test_wallpaper.py   # Tests for rendering logic  
```

> [!NOTE]
> - `src/` layout prevents accidental imports from the working directory.
> - Tests are kept outside `src/`, as recommended by PyPA.
> - Heavy I/O (SRTM downloads, file writes) is mocked in tests.
> `test_cli.py` is optional but useful to validate argument wiring and integration.

---

## Data Sources

* Elevation data: NASA SRTM (via `elevation` library)
  * Resolution: ~30m (SRTM1)

---

## License

GNU General Public License (see `LICENSE` file).

---

## Roadmap

- [x] CLI tool  
- [ ] GUI frontend  
- [ ] Multiple contour styles  
- [ ] Export presets for common screen sizes  
- [ ] Batch wallpaper generation  
- [ ] Optional vector output (SVG)  

---

## Acknowledgements

* NASA / USGS for SRTM data
* GDAL and rasterio projects
* matplotlib and scipy communities

