# Isohypses Wallpaper Generator

Isohypses Wallpaper Generator is a command-line application that creates high-resolution desktop wallpapers based on topographic contour lines (isohypses) derived from SRTM elevation data.

Given a geographic location, a zoom level, and a target screen resolution, the application automatically fetches elevation data, computes contour lines, and renders a wallpaper-sized image that fits the screen exactly.

The project is designed CLI-first, with a modular architecture that will later support a graphical user interface.

---

## Motivation

Topographic contour lines are a visually clean and information-rich way to represent terrain. This project aims to make it easy to turn real-world elevation data into aesthetically pleasing desktop backgrounds, while keeping the tool simple, reproducible, and free of proprietary data sources.

---

## Features

- Global elevation coverage using SRTM data
- Zoom-based geographic scale (map-style zoom levels)
- Exact-fit wallpapers for any screen resolution
- Multiple visual styles (extensible)
- Automatic contour interval selection
- Deterministic output for reproducibility
- Local caching of elevation data

---

## How It Works

1. The user specifies a geographic center (latitude and longitude).
2. A zoom level defines the map scale (meters per pixel).
3. The screen resolution determines the geographic extent.
4. SRTM elevation data is downloaded and clipped to that extent.
5. Contour lines are generated from the elevation raster.
6. The contours are rendered into a wallpaper-sized image.

---

## Installation

### Requirements

- Python 3.9 or newer
- Poetry

If Poetry is not installed, see the official documentation:  
https://python-poetry.org/docs/#installation

---

### Clone the repository

```bash
git clone https://github.com/yourusername/isohypses-wallpaper.git
cd isohypses-wallpaper
````

---

### Install dependencies with Poetry

```bash
poetry install
```

This will:

* Create an isolated virtual environment
* Install all runtime and development dependencies
* Lock dependency versions in `poetry.lock`

Activate the virtual environment:

```bash
poetry shell
```

Or run commands directly:

```bash
poetry run isohypses-wallpaper --help
```

---

## Command Line Usage

Basic usage:

```bash
poetry run isohypses-wallpaper generate \
  --lat 46.5763 \
  --lon 7.9904 \
  --zoom 11 \
  --width 3840 \
  --height 2160 \
  --output wallpaper.png
```

---

### Required arguments

* `--lat`
  Latitude of the image center.

* `--lon`
  Longitude of the image center.

* `--zoom`
  Map-style zoom level defining the geographic scale.

* `--width`
  Output image width in pixels.

* `--height`
  Output image height in pixels.

* `--output`
  Path to the output image file.

---

### Optional arguments

* `--style`
  Visual style preset (default: minimal).

* `--interval`
  Contour interval in meters. If omitted, the interval is chosen automatically.

* `--cache-dir`
  Directory used to cache downloaded elevation data.

---

## Zoom Levels and Scale

Zoom levels follow the standard Web Mercator convention.
Lower zoom levels cover larger areas with less detail, higher zoom levels cover smaller areas with more detail.

Typical usage ranges:

* Zoom 7–9: large regions, mountain ranges
* Zoom 10–11: cities and surrounding terrain
* Zoom 12–13: valleys, ridges, local landscapes

Very high zoom levels may exceed the native resolution of SRTM data and will not add real terrain detail.

---

## Elevation Data

This application uses Shuttle Radar Topography Mission (SRTM) data:

* Approximate resolution: 30 meters
* Units: meters above sea level
* Coverage: most land areas between 60°N and 60°S

SRTM data is free and publicly available.

---

## Project Structure

```text
isohypses_wallpaper/
├── src/
│   └── isohypses_wallpaper/
│       ├── cli.py
│       ├── config.py
│       ├── scale.py
│       ├── geometry.py
│       ├── srtm.py
│       ├── contours.py
│       ├── render.py
│       └── styles/
├── tests/
├── README.md
├── pyproject.toml
└── poetry.lock
```

---

## Docker (Optional)

For a fully reproducible environment, the application can be run in Docker.

### Build the image

```bash
docker build -t isohypses-wallpaper .
```

### Run the container

```bash
docker run --rm \
  -v $(pwd):/data \
  isohypses-wallpaper generate \
  --lat 46.5763 \
  --lon 7.9904 \
  --zoom 11 \
  --width 3840 \
  --height 2160 \
  --output /data/wallpaper.png
```

The output image will be written to the local directory.

---

## Development Workflow

* Install dependencies: `poetry install`
* Add a dependency: `poetry add <package>`
* Run commands: `poetry run <command>`
* Run tests: `poetry run pytest`
* Build Docker image for reproducibility or CI

---

## Design Principles

* Clear separation between data handling, geometry, and rendering
* Configuration-driven core logic
* Minimal assumptions about output usage
* Extensible architecture for styles and interfaces

---

## Limitations

* SRTM data does not cover polar regions
* Fine zoom levels may exceed the native resolution of the DEM
* Rendering is raster-based; vector output is not currently supported

---

## Roadmap

* Additional visual styles
* Improved contour smoothing and simplification
* Configuration presets
* Graphical user interface
* Optional SVG export

---

## License

This project is released under an open-source license.
See the LICENSE file for details.
