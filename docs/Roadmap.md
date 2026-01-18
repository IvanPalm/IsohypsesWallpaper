# Roadmap

This document outlines the planned evolution of **IsohypsesWallpaper**, starting from the current CLI-based prototype toward a more complete and user-friendly tool.

The version numbers are indicative and may change as development progresses.

---

## Version 0.1.x – Foundation

**Status:** Implemented  
**Focus:** Core functionality and correctness

### Features
- CLI tool for generating wallpapers from SRTM elevation data
- Zoom-based scale calculation
- Bounding box computation from center + screen size
- DEM download and clipping via SRTM
- Contour line rendering
- Uniform background color
- Custom output resolution
- Automated tests for core modules

### Rationale
This version establishes a solid technical base. The goal is to make sure the math, data handling, and rendering pipeline are correct before adding more features.

---

## Version 0.2.0 – Metadata & Presets

**Status:** Planned  
**Focus:** Reproducibility and ease of use

### Planned features
- Embed generation parameters into image metadata:
  - latitude, longitude
  - zoom level
  - contour interval
  - colors
  - generation date
- Presets for common screen sizes:
  - 1080p
  - 1440p
  - 4K
  - Ultrawide
- Keep full support for custom resolutions

### Rationale
Metadata makes wallpapers easier to reproduce and organize later.  
Screen-size presets remove friction for common use cases while keeping flexibility for advanced users.

---

## Version 0.3.0 – Color Themes

**Status:** Planned  
**Focus:** Visual quality and usability

### Planned features
- Built-in color themes (background + contour combinations)
- Clear naming for themes (e.g. “Dark Minimal”, “Paper Map”)
- Ability to override any theme with custom colors
- CLI option to list available themes

### Rationale
Choosing colors is one of the most visible parts of the output. Presets help users get good-looking results quickly, while custom colors keep creative freedom.

---

## Version 0.4.0 – Batch Generation

**Status:** Planned  
**Focus:** Automation and productivity

### Planned features
- Generate multiple wallpapers in one run:
  - multiple locations
  - multiple zoom levels
  - multiple color themes
- Optional configuration file (YAML or TOML)
- Automatic output naming

### Rationale
Batch mode makes the tool useful for collections, experiments, and automation. It also prepares the ground for future GUI features.

---

## Version 0.5.0 – Vector Output (SVG)

**Status:** Planned  
**Focus:** High-quality and scalable output

### Planned features
- Optional SVG output for contour lines
- Resolution-independent output
- Support for large-format printing and design workflows

### Rationale
Vector output allows infinite scaling and post-processing in design tools. This expands the project beyond wallpapers into cartography and graphic design use cases.

---

## Version 0.6.0 – GUI Frontend

**Status:** Planned  
**Focus:** Accessibility and interactivity

### Planned features
- Cross-platform GUI (desktop-first)
- Interactive map preview
- Live updates when changing parameters
- Export using the same core engine as the CLI

### Rationale
A GUI makes the tool accessible to non-technical users and supports exploration and experimentation. Keeping the CLI and GUI on top of the same core logic avoids code duplication.

---

## Long-term ideas (post 1.0)

**Status:** Ideas  
**Focus:** Expansion and experimentation

- Multiple DEM sources (Copernicus, local datasets)
- Offline mode with cached tiles
- Style editor for advanced users
- Output based on non-DEM data (isobars, etc)
- Animated outputs (time-based zooms or rotations)
