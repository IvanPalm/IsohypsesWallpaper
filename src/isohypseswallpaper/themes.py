# src/isohypseswallpaper/themes.py

from typing import Literal

ThemeType = Literal["static", "dynamic"]

COLOR_THEMES = {
    "dark_minimal": {
        "background": "#1a1a1a",
        "contour": "white",
        "type": "static",
    },
    "paper_map": {
        "background": "#f0e6d2",
        "contour": "#555555",
        "type": "static",
    },
    "mountain_palette": {
        "background": ["#003300", "#88ff88"],
        "contour": ["#552200", "#ffeeaa"],
        "type": "dynamic",
    },
    "sunset_valley": {
        "background": ["#ffccaa", "#220022"],
        "contour": ["#ff4444", "#ffffaa"],
        "type": "dynamic",
    },
}

def list_themes() -> list[str]:
    """Return a list of available theme names."""
    return list(COLOR_THEMES.keys())

def get_theme(theme_name: str):
    """Return the theme dictionary by name."""
    if theme_name not in COLOR_THEMES:
        raise ValueError(f"Theme '{theme_name}' not found. Available: {list_themes()}")
    return COLOR_THEMES[theme_name]
