# Installation

## Requirements

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

## Install with Poetry (development)

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/isohypseswallpaper.git
cd isohypseswallpaper
poetry install
```