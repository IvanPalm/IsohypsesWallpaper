# Usage

After installation, the CLI tool is available as:

```bash
isohypses-wallpaper
```

## Basic example

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

### Command-line options

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

## Development

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

### Run tests

```bash
poetry run pytest
```
