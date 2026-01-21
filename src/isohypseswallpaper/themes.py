"""
Color themes for Isohypses Wallpaper.

Each theme defines:
- background: a single color OR a list of colors (altitude-based gradient)
- contour: a single color OR a list of colors (altitude-based gradient)

Themes range from minimalist cartographic styles to expressive,
elevation-driven artistic palettes.
"""

from typing import Dict, List, Union

Color = Union[str, List[str]]

THEMES: Dict[str, Dict[str, Color]] = {
    # ------------------------------------------------------------------
    # Minimalist / Two-Color Themes
    # ------------------------------------------------------------------

    "mono_ink": {
        "background": [
            "#0f0f0f",
            "#2a2a2a",
        ],
        "contour": "#ffffff",
    },

    "paper_charcoal": {
        "background": [
            "#f7f3e9",
            "#ded6c8",
        ],
        "contour": "#2b2b2b",
    },

    "blueprint_minimal": {
        "background": [
            "#001f3f",
            "#003566",
        ],
        "contour": "#a8dadc",
    },

    "desert_minimal": {
        "background": [
            "#f4e8d1",
            "#d6b98c",
        ],
        "contour": "#6b4f2c",
    },

    "night_glow": {
        "background": [
            "#020617",
            "#111827",
        ],
        "contour": [
            "#7dd3fc",
            "#e0f2fe",
        ],
    },

    # ------------------------------------------------------------------
    # Retro / Synth / Vaporwave
    # ------------------------------------------------------------------

    "neon_90s_dark": {
        "background": [
            "#050014",
            "#12003a",
            "#00f0ff",
        ],
        "contour": [
            "#ff2bd6",
            "#f8ff00",
        ],
    },

    "neon_90s_light": {
        "background": [
            "#f5fbff",
            "#b8fbff",
            "#ffb3ec",
        ],
        "contour": [
            "#6a00ff",
            "#ff2bd6",
        ],
    },

    "vhs_static": {
        "background": [
            "#1c1c1c",
            "#5e5e5e",
            "#d6d6d6",
        ],
        "contour": [
            "#ff005d",
            "#00e5ff",
        ],
    },

    # ------------------------------------------------------------------
    # Natural / Earth
    # ------------------------------------------------------------------

    "lichen_forest": {
        "background": [
            "#0f1f14",
            "#2f4f2f",
            "#6b8e23",
            "#cde77f",
        ],
        "contour": [
            "#f2e8cf",
            "#a3b18a",
        ],
    },

    "autumn_ridge": {
        "background": [
            "#2b1300",
            "#6b2d0a",
            "#b45309",
            "#f4a261",
        ],
        "contour": [
            "#fff3e0",
            "#ffd166",
        ],
    },

    "polar_night": {
        "background": [
            "#020617",
            "#0b1c2d",
            "#164e63",
            "#38bdf8",
        ],
        "contour": [
            "#e0f2fe",
            "#7dd3fc",
        ],
    },

    # ------------------------------------------------------------------
    # Scientific / Cartographic
    # ------------------------------------------------------------------

    "bathymetry_blue": {
        "background": [
            "#001219",
            "#003049",
            "#005f73",
            "#94d2bd",
        ],
        "contour": [
            "#e9d8a6",
            "#ffd166",
        ],
    },

    "paper_map": {
        "background": [
            "#f8f4e3",
            "#e8dfc8",
            "#d6cbb0",
        ],
        "contour": [
            "#5a4632",
            "#9c6b30",
        ],
    },

    # ------------------------------------------------------------------
    # Expressive / Atmospheric
    # ------------------------------------------------------------------

    "volcanic_glass": {
        "background": [
            "#050505",
            "#2b0a0a",
            "#5c0f0f",
            "#ff4500",
        ],
        "contour": [
            "#ffae00",
            "#fff1c1",
        ],
    },

    "orbital_dust": {
        "background": [
            "#0d0221",
            "#2e1f47",
            "#6a4c93",
            "#cdb4db",
        ],
        "contour": [
            "#eae4ff",
            "#ffd6ff",
        ],
    },

    "aurora_borealis": {
        "background": [
            "#020617",
            "#064e3b",
            "#10b981",
            "#99f6e4",
        ],
        "contour": [
            "#ecfeff",
            "#a7f3d0",
        ],
    },
}


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------

def get_theme(name: str) -> Dict[str, Color]:
    """
    Retrieve a theme by name.

    Raises
    ------
    KeyError
        If the theme does not exist.
    """
    if name not in THEMES:
        raise KeyError(
            f"Unknown theme '{name}'. "
            f"Available themes: {', '.join(sorted(THEMES.keys()))}"
        )
    return THEMES[name]


def list_themes() -> list[str]:
    """
    Return a sorted list of available theme names.
    """
    return sorted(THEMES.keys())
