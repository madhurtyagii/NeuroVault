# NeuroVault - Premium UI Design System (Perplexity-inspired)

# Elite Color Palette
COLORS = {
    # Backgrounds (ultra smooth dark)
    'bg_primary': '#0b0d0f',       # Almost black (like Perplexity)
    'bg_secondary': '#16181c',     # Very subtle gray
    'bg_tertiary': '#1c1f24',      # Card background
    'bg_hover': '#23262c',         # Hover state
    
    # Accents (SUBTLE professional)
    'accent_primary': '#5b8def',   # Soft professional blue
    'accent_hover': '#4d7dd9',     # Slightly darker blue
    # 'accent_glow': '#5b8def22',    # Glow effect (22 = subtle transparency)
    
    # Text (maximum readability)
    'text_primary': '#e5e5e6',     # Almost white
    'text_secondary': '#9b9c9e',   # Medium gray
    'text_tertiary': '#6e7175',    # Subtle gray
    'text_dim': '#4a4d51',         # Very dim
    
    # Status (softer tones)
    'success': '#0dbb87',
    'error': '#ef5350',
    'warning': '#ff9f43',
    
    # Borders (barely visible)
    'border_subtle': '#2a2d32',
    'border_medium': '#35383e',
}

# Button Styles - Premium Feel
BUTTON_STYLES = {
    'primary': {
        'fg_color': COLORS['accent_primary'],
        'hover_color': COLORS['accent_hover'],
        'text_color': '#ffffff',
        'corner_radius': 10,
        'height': 40,
        'font': ('Inter', 12, 'normal'),  # Modern font
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
        'font': ('Inter', 12, 'normal'),
    },
    'danger': {
        'fg_color': COLORS['error'],
        'hover_color': '#d32f2f',
        'text_color': '#ffffff',
        'corner_radius': 10,
        'height': 40,
        'font': ('Inter', 12, 'normal'),
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

# Typography - Hierarchy
TEXT_STYLES = {
    'hero': ('Inter', 28, 'bold'),           # Main titles
    'title': ('Inter', 20, 'bold'),          # Section titles
    'subtitle': ('Inter', 16, 'bold'),       # Subtitles
    'heading': ('Inter', 14, 'bold'),        # Card headings
    'body': ('Inter', 13, 'normal'),         # Body text
    'body_small': ('Inter', 12, 'normal'),   # Small text
    'caption': ('Inter', 11, 'normal'),      # Captions/metadata
    'mono': ('JetBrains Mono', 12, 'normal'), # Code/mono
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

# Input Styles - Clean & Modern
INPUT_STYLES = {
    'fg_color': COLORS['bg_secondary'],
    'border_color': COLORS['border_medium'],
    'border_width': 1,
    'text_color': COLORS['text_primary'],
    'placeholder_text_color': COLORS['text_tertiary'],
    'corner_radius': 10,
    'height': 48,  # Taller for better UX
    'font': TEXT_STYLES['body'],
}

# Scrollbar Styles
SCROLLBAR_STYLES = {
    'fg_color': COLORS['bg_primary'],
    'button_color': COLORS['border_medium'],
    'button_hover_color': COLORS['accent_primary'],
}
