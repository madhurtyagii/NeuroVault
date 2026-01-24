# NeuroVault - Premium UI Design System with Full Theme Support

import json
from pathlib import Path

# Config file for theme preference
CONFIG_FILE = Path(__file__).parent.parent / "data" / "config.json"

# Dark Mode Colors
DARK_COLORS = {
    'bg_primary': '#0b0d0f',
    'bg_secondary': '#16181c',
    'bg_tertiary': '#1c1f24',
    'bg_hover': '#23262c',
    'accent_primary': '#5b8def',
    'accent_hover': '#4d7dd9',
    'text_primary': '#e5e5e6',
    'text_secondary': '#9b9c9e',
    'text_tertiary': '#6e7175',
    'text_dim': '#4a4d51',
    'border_subtle': '#2a2d32',
    'border_medium': '#35383e',
    'success': '#0dbb87',
    'error': '#ef5350',
    'warning': '#ff9f43',
}

# Light Mode Colors
LIGHT_COLORS = {
    'bg_primary': '#ffffff',
    'bg_secondary': '#f8fafc',
    'bg_tertiary': '#f1f5f9',
    'bg_hover': '#e2e8f0',
    'accent_primary': '#3b82f6',
    'accent_hover': '#2563eb',
    'text_primary': '#0f172a',
    'text_secondary': '#475569',
    'text_tertiary': '#64748b',
    'text_dim': '#94a3b8',
    'border_subtle': '#e2e8f0',
    'border_medium': '#cbd5e1',
    'success': '#10b981',
    'error': '#ef4444',
    'warning': '#f59e0b',
}

def load_theme():
    """Load theme preference from config file"""
    try:
        CONFIG_FILE.parent.mkdir(exist_ok=True)
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('theme', 'dark')
    except:
        pass
    return 'dark'

def save_theme(theme):
    """Save theme preference to config file"""
    try:
        CONFIG_FILE.parent.mkdir(exist_ok=True)
        config = {'theme': theme}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except:
        pass

# Load current theme
CURRENT_THEME = load_theme()
COLORS = DARK_COLORS.copy() if CURRENT_THEME == 'dark' else LIGHT_COLORS.copy()

# Button Styles
BUTTON_STYLES = {
    'primary': {
        'fg_color': COLORS['accent_primary'],
        'hover_color': COLORS['accent_hover'],
        'text_color': '#ffffff',
        'corner_radius': 10,
        'height': 40,
        'font': ('Segoe UI', 12, 'normal'),
        'border_width': 0,
    },
    'secondary': {
        'fg_color': COLORS['bg_tertiary'],
        'hover_color': COLORS['bg_hover'],
        'text_color': COLORS['text_secondary'],
        'border_width': 1,
        'border_color': COLORS['border_medium'],
        'corner_radius': 10,
        'height': 40,
        'font': ('Segoe UI', 12, 'normal'),
    },
    'danger': {
        'fg_color': COLORS['error'],
        'hover_color': '#d32f2f' if CURRENT_THEME == 'dark' else '#dc2626',
        'text_color': '#ffffff',
        'corner_radius': 10,
        'height': 40,
        'font': ('Segoe UI', 12, 'normal'),
        'border_width': 0,
    },
}

# Frame Styles
FRAME_STYLES = {
    'card': {
        'fg_color': COLORS['bg_tertiary'],
        'corner_radius': 12,
        'border_width': 1,
        'border_color': COLORS['border_subtle'],
    },
    'card_elevated': {
        'fg_color': COLORS['bg_secondary'],
        'corner_radius': 16,
        'border_width': 1,
        'border_color': COLORS['border_medium'],
    },
}

# Typography
TEXT_STYLES = {
    'hero': ('Segoe UI', 28, 'bold'),
    'title': ('Segoe UI', 20, 'bold'),
    'subtitle': ('Segoe UI', 16, 'bold'),
    'heading': ('Segoe UI', 14, 'bold'),
    'body': ('Segoe UI', 13, 'normal'),
    'body_small': ('Segoe UI', 12, 'normal'),
    'caption': ('Segoe UI', 11, 'normal'),
    'mono': ('Consolas', 12, 'normal'),
}

# Tab Styles
TAB_STYLES = {
    'fg_color': COLORS['bg_primary'],
    'segmented_button_fg_color': COLORS['bg_secondary'],
    'segmented_button_selected_color': COLORS['accent_primary'],
    'segmented_button_selected_hover_color': COLORS['accent_hover'],
    'segmented_button_unselected_color': COLORS['bg_secondary'],
    'segmented_button_unselected_hover_color': COLORS['bg_tertiary'],
    'text_color': COLORS['text_secondary'],
    'text_color_disabled': COLORS['text_dim'],
}

# Input Styles
INPUT_STYLES = {
    'fg_color': COLORS['bg_secondary'],
    'border_color': COLORS['border_medium'],
    'border_width': 1,
    'text_color': COLORS['text_primary'],
    'placeholder_text_color': COLORS['text_tertiary'],
    'corner_radius': 10,
    'height': 48,
    'font': TEXT_STYLES['body'],
}

# Scrollbar Styles
SCROLLBAR_STYLES = {
    'fg_color': COLORS['bg_primary'],
    'button_color': COLORS['border_medium'],
    'button_hover_color': COLORS['accent_primary'],
}
