"""
Design Tokens: The Sovereign Intelligence Framework
Monastic Brutalism meets high-stakes intelligence
"""

from typing import Dict, Tuple
from dataclasses import dataclass

# Color Palette - Midnight Tonal Scale
COLORS = {
    # Surface Hierarchy
    "surface_lowest": "#0c0e14",
    "surface_dim": "#111319",
    "surface_container_low": "#191b22",
    "surface_container": "#1e1f26",
    "surface_container_high": "#282a30",
    "surface_container_highest": "#33343b",

    # Accents & Status
    "primary": "#ffb867",  # Amber - Live status, critical CTAs
    "primary_container": "#d4840a",  # Darker amber for buttons
    "on_primary": "#ffffff",
    "on_primary_fixed_variant": "#673d00",

    # Secondary & Tertiary
    "secondary": "#a08d7b",  # Silver
    "tertiary": "#9dd3aa",  # Positive/Green
    "error": "#ffb4ab",  # Negative/Red

    # Text & Outlines
    "on_surface": "#e2e2eb",  # Off-white (prevent retina burn)
    "outline": "#a08d7b",
    "outline_variant": "#534435",  # Ghost border color
}

# Typography
FONTS = {
    "logo": ("Barlow Condensed", "sans-serif"),
    "headline": ("Lora", "serif"),  # Editorial authority
    "body": ("Lora", "serif"),  # Editorial narrative
    "data": ("JetBrains Mono", "monospace"),  # Big numbers, coordinates
    "utility": ("IBM Plex Mono", "monospace"),  # Labels, tab strips
}

# Type Scale
TYPOGRAPHY = {
    "h1": {"font": "Lora", "size": "3.5rem", "weight": 700, "line_height": 1.2},
    "h2": {"font": "Lora", "size": "2.5rem", "weight": 700, "line_height": 1.2},
    "h3": {"font": "Lora", "size": "2rem", "weight": 700, "line_height": 1.3},
    "h4": {"font": "Lora", "size": "1.5rem", "weight": 700, "line_height": 1.3},
    "h5": {"font": "Lora", "size": "1.25rem", "weight": 600, "line_height": 1.4},
    "h6": {"font": "Lora", "size": "1rem", "weight": 600, "line_height": 1.4},
    "label_md": {"font": "IBM Plex Mono", "size": "0.75rem", "weight": 700, "line_height": 1.5, "letter_spacing": 0.5},  # All caps
    "label_sm": {"font": "IBM Plex Mono", "size": "0.625rem", "weight": 700, "line_height": 1.5},
    "body_lg": {"font": "Lora", "size": "1.125rem", "weight": 400, "line_height": 1.6},
    "body_md": {"font": "Lora", "size": "1rem", "weight": 400, "line_height": 1.5},
    "body_sm": {"font": "Lora", "size": "0.875rem", "weight": 400, "line_height": 1.5},
    "data_lg": {"font": "JetBrains Mono", "size": "1.25rem", "weight": 700, "line_height": 1.4},
    "data_md": {"font": "JetBrains Mono", "size": "0.875rem", "weight": 600, "line_height": 1.4},
    "data_sm": {"font": "JetBrains Mono", "size": "0.75rem", "weight": 600, "line_height": 1.4},
}

# Spacing Scale
SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "12px",
    "lg": "16px",
    "xl": "24px",
    "2xl": "32px",
    "3xl": "48px",
}

# Elevation & Depth
SHADOWS = {
    "ghost_border": f"0 0 0 1px {COLORS['outline_variant']}",  # 15% opacity via CSS
    "tactical_glass": "backdrop-filter: blur(12px);",
    "ambient_depth": "0 2px 8px rgba(0, 0, 0, 0.3);",
}

# Animation
TRANSITIONS = {
    "panel": "cubic-bezier(0.4, 0, 0.2, 1)",  # Heavy, hydraulic feel
    "interaction": "100ms ease-out",
    "state_change": "0ms",  # Mechanical switch - no transition
}

# Animation keyframes
KEYFRAMES = {
    "amber_pulse": {
        "0%": {"box_shadow": f"0 0 20px {COLORS['primary']} 10%"},
        "50%": {"box_shadow": f"0 0 20px {COLORS['primary']} 20%"},
        "100%": {"box_shadow": f"0 0 20px {COLORS['primary']} 10%"},
    },
    "blink_cursor": {
        "0%, 49%": {"opacity": "1"},
        "50%, 100%": {"opacity": "0"},
    },
}

# Border Radius (ZERO - hard corners for precision)
RADIUS = {
    "none": "0px",
    "sm": "2px",
}

# Layout
LAYOUT = {
    "sidebar_width": "320px",
    "max_content_width": "1920px",
    "gutter": "24px",
    "panel_gap": "16px",
}

@dataclass
class ThemeToken:
    """Single design token with CSS variable support"""
    name: str
    value: str
    css_var: str = None

    def __post_init__(self):
        if not self.css_var:
            self.css_var = f"--{self.name.lower().replace('_', '-')}"


def generate_css_variables() -> str:
    """Generate CSS custom properties from tokens"""
    css = ":root {\n"

    # Colors
    for name, value in COLORS.items():
        css += f"  --color-{name.lower().replace('_', '-')}: {value};\n"

    # Typography
    for style, props in TYPOGRAPHY.items():
        css += f"  --typo-{style.lower()}-font: {props['font']}, {props['font'].split(',')[1] if ',' in props['font'] else 'sans-serif'};\n"
        css += f"  --typo-{style.lower()}-size: {props['size']};\n"
        css += f"  --typo-{style.lower()}-weight: {props['weight']};\n"
        css += f"  --typo-{style.lower()}-line-height: {props['line_height']};\n"

    # Spacing
    for name, value in SPACING.items():
        css += f"  --spacing-{name}: {value};\n"

    # Layout
    for name, value in LAYOUT.items():
        css += f"  --layout-{name.lower().replace('_', '-')}: {value};\n"

    css += "}\n"
    return css


def get_tonal_transition(from_color: str, to_color: str) -> str:
    """Create a tonal shift background gradient"""
    return f"background: linear-gradient(to bottom, {from_color}, {to_color});"
