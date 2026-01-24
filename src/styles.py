# Modern UI color scheme and styles for NeuroVault

import json
from pathlib import Path

# Theme management
CONFIG_FILE = Path(__file__).parent.parent / 'data' / 'config.json'

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
    # Dark Mode Colors (YOUR ORIGINAL!)
    COLORS = {
        # Dark theme base
        'bg_primary': '#0a0e27',
        'bg_secondary': '#151b3d',
        'bg_tertiary': '#1e2749',
        
        # Accent colors
        'accent_primary': '#00d4ff',
        'accent_secondary': '#7c3aed',
        'accent_hover': '#00b8d4',
        'accent_gradient_1': '#00d4ff',
        'accent_gradient_2': '#7c3aed',
        
        # Text colors
        'text_primary': '#ffffff',
        'text_secondary': '#a0aec0',
        'text_tertiary': '#718096',
        'text_muted': '#718096',
        'text_dim': '#4a5568',
        
        # Status colors
        'success': '#10b981',
        'error': '#ef4444',
        'warning': '#f59e0b',
        'info': '#3b82f6',
        
        # UI elements
        'border': '#2d3748',
        'border_medium': '#2d3748',
        'border_subtle': '#2d3748',
        'bg_hover': '#2d3a5f',
        'hover': '#2d3a5f',
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
