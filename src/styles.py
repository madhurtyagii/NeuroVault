# Modern UI color scheme and styles for NeuroVault

import json
from pathlib import Path

# Theme management
import os

APP_DIR = Path.home() / ".neurovault"
APP_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = APP_DIR / 'config.json'

def load_theme():
    """Load theme preference from config"""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('theme', 'dark')
    except:
        pass
    return 'dark'

def save_theme(theme):
    """Save theme preference to config"""
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        config = {}
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
        config['theme'] = theme
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Error saving theme: {e}")

CURRENT_THEME = load_theme()

# Theme-based colors
if CURRENT_THEME == 'light':
    # Light Mode Colors
    COLORS = {
        # Light theme base
        'bg_primary': '#f8fafc',
        'bg_secondary': '#ffffff',
        'bg_tertiary': '#f1f5f9',
        
        # Accent colors
        'accent_primary': '#0ea5e9',
        'accent_secondary': '#8b5cf6',
        'accent_hover': '#0284c7',
        'accent_gradient_1': '#0ea5e9',
        'accent_gradient_2': '#8b5cf6',
        
        # Text colors
        'text_primary': '#0f172a',
        'text_secondary': '#475569',
        'text_tertiary': '#64748b',
        'text_muted': '#94a3b8',
        'text_dim': '#cbd5e1',
        
        # Status colors
        'success': '#10b981',
        'error': '#ef4444',
        'warning': '#f59e0b',
        'info': '#3b82f6',
        
        # UI elements
        'border': '#e2e8f0',
        'border_medium': '#cbd5e1',
        'border_subtle': '#e2e8f0',
        'bg_hover': '#e2e8f0',
        'hover': '#e2e8f0',
    }
else:
    # Dark Mode Colors - Refined & Sophisticated
    COLORS = {
        # Dark theme base - softer slate grays
        'bg_primary': '#0f1419',      # Deep charcoal (softer than navy)
        'bg_secondary': '#1a1f2e',    # Slate gray
        'bg_tertiary': '#242b3d',     # Lighter slate
        
        # Accent colors - muted indigo/violet (elegant, not harsh)
        'accent_primary': '#6366f1',   # Muted indigo
        'accent_secondary': '#8b5cf6', # Soft violet
        'accent_hover': '#818cf8',     # Lighter indigo
        'accent_gradient_1': '#6366f1',
        'accent_gradient_2': '#a855f7',
        
        # Message colors
        'user_message': '#4f46e5',     # User bubble - deeper indigo
        'ai_message': '#1e2433',       # AI message background
        'ai_message_border': '#2d3548', # AI message border
        
        # Text colors - softer contrast
        'text_primary': '#e2e8f0',     # Off-white (easier on eyes)
        'text_secondary': '#94a3b8',   # Muted gray
        'text_tertiary': '#64748b',    # Dimmer gray
        'text_muted': '#475569',       # Very muted
        'text_dim': '#334155',         # Subtle
        
        # Status colors - slightly muted versions
        'success': '#22c55e',          # Green
        'error': '#f43f5e',            # Rose red (softer than pure red)
        'warning': '#f59e0b',          # Amber
        'info': '#6366f1',             # Match accent
        
        # UI elements
        'border': '#2d3548',           # Subtle border
        'border_medium': '#3d4660',    # Medium border
        'border_subtle': '#252d3d',    # Very subtle
        'bg_hover': '#2a3244',         # Hover state
        'hover': '#2a3244',
        
        # Special
        'code_bg': '#1a1f2b',          # Code block background
        'scrollbar': '#3d4660',        # Scrollbar color
    }

# Button styles
BUTTON_STYLES = {
    'primary': {
        'fg_color': COLORS['accent_primary'],
        'hover_color': COLORS['accent_hover'],
        'text_color': COLORS['bg_primary'],
        'corner_radius': 8,
        'height': 36,
        'font': ('Segoe UI', 12, 'bold'),
    },
    'secondary': {
        'fg_color': COLORS['bg_tertiary'],
        'hover_color': COLORS['hover'],
        'text_color': COLORS['text_primary'],
        'border_width': 2,
        'border_color': COLORS['accent_primary'],
        'corner_radius': 8,
        'height': 36,
        'font': ('Segoe UI', 12),
    },
    'danger': {
        'fg_color': COLORS['error'],
        'hover_color': '#dc2626',
        'text_color': COLORS['text_primary'],
        'corner_radius': 8,
        'height': 36,
        'font': ('Segoe UI', 12, 'bold'),
    },
}

# Frame styles
FRAME_STYLES = {
    'main': {
        'fg_color': COLORS['bg_primary'],
        'corner_radius': 0,
    },
    'card': {
        'fg_color': COLORS['bg_tertiary'],
        'corner_radius': 12,
        'border_width': 1,
        'border_color': COLORS['border'],
    },
    'sidebar': {
        'fg_color': COLORS['bg_secondary'],
        'corner_radius': 0,
    },
}

# Text styles
TEXT_STYLES = {
    'title': ('Segoe UI', 24, 'bold'),
    'subtitle': ('Segoe UI', 16, 'bold'),
    'heading': ('Segoe UI', 14, 'bold'),
    'body': ('Segoe UI', 12),
    'body_small': ('Segoe UI', 11),
    'small': ('Segoe UI', 10),
    'caption': ('Segoe UI', 9),
    'code': ('Consolas', 11),
}

# Tab styles
TAB_STYLES = {
    'fg_color': COLORS['bg_secondary'],
    'segmented_button_fg_color': COLORS['bg_tertiary'],
    'segmented_button_selected_color': COLORS['accent_primary'],
    'segmented_button_selected_hover_color': COLORS['accent_hover'],
    'segmented_button_unselected_color': COLORS['bg_tertiary'],
    'segmented_button_unselected_hover_color': COLORS['hover'],
    'text_color': COLORS['text_primary'],
    'text_color_disabled': COLORS['text_muted'],
}

# Entry/Input styles
INPUT_STYLES = {
    'fg_color': COLORS['bg_tertiary'],
    'border_color': COLORS['border'],
    'text_color': COLORS['text_primary'],
    'placeholder_text_color': COLORS['text_muted'],
    'corner_radius': 8,
    'height': 40,
    'font': TEXT_STYLES['body'],
}

# Scrollbar styles
SCROLLBAR_STYLES = {
    'fg_color': COLORS['bg_secondary'],
    'button_color': COLORS['accent_primary'],
    'button_hover_color': COLORS['accent_hover'],
}
