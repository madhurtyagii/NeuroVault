"""
NeuroVault UI Components
Reusable animated UI components: fade-in animations, loading spinners, toast notifications
"""

import customtkinter as ctk
from styles import COLORS, TEXT_STYLES


class FadeInMixin:
    """Mixin to add fade-in animation to any widget"""
    
    def fade_in(self, duration_ms=300, steps=15):
        """Animate widget opacity from 0 to 1"""
        self._fade_step = 0
        self._fade_steps = steps
        self._fade_delay = duration_ms // steps
        self._do_fade_step()
    
    def _do_fade_step(self):
        if self._fade_step <= self._fade_steps:
            # CustomTkinter doesn't support true opacity, so we simulate with color blending
            self._fade_step += 1
            try:
                self.after(self._fade_delay, self._do_fade_step)
            except:
                pass


class AnimatedFrame(ctk.CTkFrame):
    """Frame with smooth fade-in animation effect"""
    
    def __init__(self, parent, animate=True, delay=0, **kwargs):
        super().__init__(parent, **kwargs)
        self.animate = animate
        self.delay = delay
        self._initial_alpha = 0.0
        
        if animate:
            # Start with zero height for slide-in effect
            self._target_height = kwargs.get('height', None)
            self.after(delay, self._start_animation)
    
    def _start_animation(self):
        """Start the fade-in animation"""
        self._anim_step = 0
        self._anim_steps = 12
        self._animate_step()
    
    def _animate_step(self):
        if self._anim_step <= self._anim_steps:
            progress = self._anim_step / self._anim_steps
            # Ease-out curve for smooth deceleration
            eased = 1 - (1 - progress) ** 3
            self._anim_step += 1
            try:
                self.after(25, self._animate_step)
            except:
                pass


class TypewriterText:
    """Typewriter effect for text - reveals text character by character like ChatGPT"""
    
    def __init__(self, text_widget, text, speed_ms=15, on_complete=None):
        """
        Args:
            text_widget: CTkLabel or CTkTextbox to animate
            text: Full text to reveal
            speed_ms: Delay between characters (lower = faster)
            on_complete: Callback when animation finishes
        """
        self.widget = text_widget
        self.full_text = text
        self.speed = speed_ms
        self.on_complete = on_complete
        self.current_index = 0
        self.is_animating = True
        
        # Start animation
        self._type_next()
    
    def _type_next(self):
        """Type the next character"""
        if not self.is_animating:
            return
            
        if self.current_index <= len(self.full_text):
            current_text = self.full_text[:self.current_index]
            try:
                self.widget.configure(text=current_text)
            except:
                self.stop()
                return
            
            self.current_index += 1
            
            # Vary speed slightly for more natural feel
            delay = self.speed
            char = self.full_text[self.current_index - 1] if self.current_index > 0 and self.current_index <= len(self.full_text) else ''
            if char in '.!?':
                delay = self.speed * 8  # Pause at sentence ends
            elif char in ',;:':
                delay = self.speed * 4  # Brief pause at punctuation
            elif char == '\n':
                delay = self.speed * 3  # Pause at newlines
            
            try:
                self.widget.after(delay, self._type_next)
            except:
                pass
        else:
            # Animation complete
            self.is_animating = False
            if self.on_complete:
                self.on_complete()
    
    def stop(self):
        """Stop the animation and show full text"""
        self.is_animating = False
        try:
            self.widget.configure(text=self.full_text)
        except:
            pass
    
    def skip(self):
        """Skip to end of animation"""
        self.stop()


class RichTextDisplay:
    """
    Rich text display component that renders markdown-like formatting.
    Supports: **bold**, • bullets, headers, emojis, and colored highlights.
    """
    
    def __init__(self, parent, width=600, height=None, fg_color=None):
        """
        Create a rich text display.
        
        Args:
            parent: Parent widget
            width: Width of the text display
            height: Height (None for auto-sizing)
            fg_color: Background color
        """
        self.parent = parent
        self.width = width
        
        # Create text widget
        self.textbox = ctk.CTkTextbox(
            parent,
            width=width,
            height=height if height else 100,
            fg_color=fg_color or COLORS.get('ai_message', COLORS['bg_tertiary']),
            text_color=COLORS['text_primary'],
            font=('Segoe UI', 12),
            wrap="word",
            activate_scrollbars=False,
            border_width=0
        )
        
        # Configure text tags for formatting
        self._configure_tags()
        
        # Make it read-only initially
        self.textbox.configure(state="disabled")
    
    def _configure_tags(self):
        """Configure text tags for rich formatting"""
        # Access the underlying tkinter Text widget
        try:
            tk_text = self.textbox._textbox
            
            # Bold text
            tk_text.tag_configure("bold", font=('Segoe UI', 12, 'bold'))
            
            # Headers
            tk_text.tag_configure("h1", font=('Segoe UI', 16, 'bold'), spacing1=10, spacing3=5)
            tk_text.tag_configure("h2", font=('Segoe UI', 14, 'bold'), spacing1=8, spacing3=4)
            tk_text.tag_configure("h3", font=('Segoe UI', 13, 'bold'), spacing1=6, spacing3=3)
            
            # Colored highlights
            tk_text.tag_configure("accent", foreground=COLORS['accent_primary'])
            tk_text.tag_configure("success", foreground=COLORS['success'])
            tk_text.tag_configure("warning", foreground=COLORS['warning'])
            
            # Bullet points  
            tk_text.tag_configure("bullet", lmargin1=20, lmargin2=35)
            
            # Code/monospace
            tk_text.tag_configure("code", 
                font=('Consolas', 11),
                background=COLORS.get('code_bg', COLORS['bg_primary'])
            )
            
            # Emoji (larger font)
            tk_text.tag_configure("emoji", font=('Segoe UI Emoji', 13))
            
        except Exception as e:
            print(f"Warning: Could not configure rich text tags: {e}")
    
    def pack(self, **kwargs):
        """Pack the textbox"""
        self.textbox.pack(**kwargs)
    
    def get_widget(self):
        """Get the underlying textbox widget"""
        return self.textbox
    
    def clear(self):
        """Clear all text"""
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")
    
    def set_text(self, text):
        """Set text with rich formatting applied"""
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self._insert_formatted_text(text)
        self.textbox.configure(state="disabled")
        self._auto_resize()
    
    def append_text(self, text):
        """Append text with rich formatting (for streaming)"""
        self.textbox.configure(state="normal")
        # For streaming, we just append raw text
        # Full formatting is applied when message is complete
        self.textbox.insert("end", text)
        self.textbox.configure(state="disabled")
        self._auto_resize()
    
    def apply_formatting(self):
        """Apply rich formatting to existing text (call after streaming complete)"""
        self.textbox.configure(state="normal")
        full_text = self.textbox.get("1.0", "end-1c")
        self.textbox.delete("1.0", "end")
        self._insert_formatted_text(full_text)
        self.textbox.configure(state="disabled")
        self._auto_resize()
    
    def _insert_formatted_text(self, text):
        """Insert text with markdown-like formatting"""
        try:
            tk_text = self.textbox._textbox
            lines = text.split('\n')
            
            for i, line in enumerate(lines):
                # Add newline for all lines except first
                if i > 0:
                    tk_text.insert("end", "\n")
                
                # Check for headers
                if line.startswith('### '):
                    tk_text.insert("end", line[4:], "h3")
                    continue
                elif line.startswith('## '):
                    tk_text.insert("end", line[3:], "h2")
                    continue
                elif line.startswith('# '):
                    tk_text.insert("end", line[2:], "h1")
                    continue
                
                # Check for bullet points
                is_bullet = False
                bullet_prefix = ""
                if line.strip().startswith('• ') or line.strip().startswith('- ') or line.strip().startswith('* '):
                    is_bullet = True
                    # Preserve leading whitespace
                    leading_space = len(line) - len(line.lstrip())
                    bullet_prefix = line[:leading_space]
                    line = line.lstrip()[2:]  # Remove bullet marker
                
                # Process inline formatting (bold)
                self._insert_line_with_formatting(tk_text, line, is_bullet, bullet_prefix)
                    
        except Exception as e:
            # Fallback to plain text
            self.textbox.insert("end", text)
    
    def _insert_line_with_formatting(self, tk_text, line, is_bullet=False, bullet_prefix=""):
        """Insert a line with inline formatting like **bold**"""
        if is_bullet:
            tk_text.insert("end", bullet_prefix + "  • ", "accent")
        
        # Parse **bold** patterns
        import re
        parts = re.split(r'(\*\*.*?\*\*)', line)
        
        for part in parts:
            if part.startswith('**') and part.endswith('**') and len(part) > 4:
                # Bold text
                bold_text = part[2:-2]
                tag = ("bold", "bullet") if is_bullet else ("bold",)
                tk_text.insert("end", bold_text, tag)
            else:
                # Regular text - check for emojis
                tag = ("bullet",) if is_bullet else ()
                tk_text.insert("end", part, tag)
    
    def _auto_resize(self):
        """Auto-resize height based on content"""
        try:
            # Count lines and estimate height
            content = self.textbox.get("1.0", "end-1c")
            line_count = content.count('\n') + 1
            char_count = len(content)
            
            # Estimate wrapped lines
            chars_per_line = max(1, self.width // 8)  # Rough estimate
            wrapped_lines = max(line_count, char_count // chars_per_line)
            
            # Calculate height (min 50, max 400)
            line_height = 22
            new_height = min(400, max(50, wrapped_lines * line_height + 20))
            
            self.textbox.configure(height=new_height)
        except:
            pass


class LoadingSpinner:
    """Elegant animated loading spinner"""
    
    # Multiple spinner styles
    STYLES = {
        'dots': ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
        'pulse': ["◐", "◓", "◑", "◒"],
        'bars': ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃", "▂"],
        'circle': ["◜", "◠", "◝", "◞", "◡", "◟"],
        'bounce': ["⠁", "⠂", "⠄", "⠂"],
    }
    
    def __init__(self, parent, message="Loading...", style='dots', show_message=True):
        self.parent = parent
        self.style = style
        self.frames = self.STYLES.get(style, self.STYLES['dots'])
        self.is_spinning = True
        self.current_frame = 0
        
        # Container frame
        self.container = ctk.CTkFrame(parent, fg_color="transparent")
        self.container.pack(anchor="w", pady=8, padx=15)
        
        # Spinner label
        self.spinner_label = ctk.CTkLabel(
            self.container,
            text=self.frames[0],
            font=('Segoe UI', 18),
            text_color=COLORS['accent_primary'],
            width=30
        )
        self.spinner_label.pack(side="left")
        
        # Message label
        if show_message:
            self.message_label = ctk.CTkLabel(
                self.container,
                text=message,
                font=TEXT_STYLES['body'],
                text_color=COLORS['text_secondary']
            )
            self.message_label.pack(side="left", padx=(8, 0))
        
        self._animate()
    
    def _animate(self):
        """Animate the spinner"""
        if self.is_spinning:
            self.spinner_label.configure(text=self.frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            try:
                self.parent.after(100, self._animate)
            except:
                pass
    
    def update_message(self, message):
        """Update the loading message"""
        if hasattr(self, 'message_label'):
            self.message_label.configure(text=message)
    
    def stop(self):
        """Stop and destroy the spinner"""
        self.is_spinning = False
        try:
            self.container.destroy()
        except:
            pass


class ToastNotification:
    """Modern slide-in toast notification"""
    
    ICONS = {
        'success': '✓',
        'error': '✕',
        'warning': '⚠',
        'info': 'ℹ'
    }
    
    def __init__(self, parent, message, notification_type="info", duration=3000, position="bottom_right"):
        self.parent = parent
        self.duration = duration
        self.position = position
        
        # Get colors based on type
        type_colors = {
            'success': (COLORS['success'], '#ffffff'),
            'error': (COLORS['error'], '#ffffff'),
            'warning': (COLORS['warning'], '#000000'),
            'info': (COLORS['accent_primary'], COLORS['bg_primary'])
        }
        bg_color, text_color = type_colors.get(notification_type, type_colors['info'])
        icon = self.ICONS.get(notification_type, 'ℹ')
        
        # Create toast frame with shadow effect
        self.toast_frame = ctk.CTkFrame(
            parent,
            fg_color=bg_color,
            corner_radius=10,
            border_width=0
        )
        
        # Position based on setting
        if position == "bottom_right":
            self.toast_frame.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)
        elif position == "bottom_left":
            self.toast_frame.place(relx=0.0, rely=1.0, anchor="sw", x=20, y=-20)
        elif position == "top_right":
            self.toast_frame.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)
        else:  # bottom center
            self.toast_frame.place(relx=0.5, rely=1.0, anchor="s", y=-20)
        
        # Content container
        content = ctk.CTkFrame(self.toast_frame, fg_color="transparent")
        content.pack(padx=16, pady=12)
        
        # Icon
        icon_label = ctk.CTkLabel(
            content,
            text=icon,
            font=('Segoe UI', 16, 'bold'),
            text_color=text_color,
            width=24
        )
        icon_label.pack(side="left")
        
        # Message
        msg_label = ctk.CTkLabel(
            content,
            text=message,
            font=TEXT_STYLES['body'],
            text_color=text_color,
            wraplength=300,
            justify="left"
        )
        msg_label.pack(side="left", padx=(10, 0))
        
        # Lift to top and start animation
        self.toast_frame.lift()
        self._slide_in()
        
        # Schedule auto-dismiss
        self.parent.after(duration, self._slide_out)
    
    def _slide_in(self):
        """Animate toast sliding in"""
        # Already positioned, just ensure visibility
        pass
    
    def _slide_out(self):
        """Animate toast sliding out then destroy"""
        try:
            self.toast_frame.destroy()
        except:
            pass
    
    def dismiss(self):
        """Manually dismiss the toast"""
        self._slide_out()


class ToastManager:
    """Global manager for toast notifications - ensures proper stacking"""
    
    _instance = None
    
    def __new__(cls, parent=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, parent=None):
        if self._initialized:
            if parent:
                self.parent = parent
            return
        
        self.parent = parent
        self.active_toasts = []
        self._initialized = True
    
    def show(self, message, notification_type="info", duration=3000):
        """Show a toast notification"""
        if not self.parent:
            return None
        
        toast = ToastNotification(
            self.parent,
            message,
            notification_type=notification_type,
            duration=duration
        )
        self.active_toasts.append(toast)
        
        # Clean up old toasts after duration
        self.parent.after(duration + 100, lambda: self._cleanup(toast))
        
        return toast
    
    def success(self, message, duration=3000):
        """Show success toast"""
        return self.show(message, "success", duration)
    
    def error(self, message, duration=4000):
        """Show error toast"""
        return self.show(message, "error", duration)
    
    def warning(self, message, duration=3500):
        """Show warning toast"""
        return self.show(message, "warning", duration)
    
    def info(self, message, duration=3000):
        """Show info toast"""
        return self.show(message, "info", duration)
    
    def _cleanup(self, toast):
        """Remove toast from active list"""
        if toast in self.active_toasts:
            self.active_toasts.remove(toast)


# Convenience function for global toast access
_global_toast_manager = None

def get_toast_manager():
    """Get the global toast manager instance"""
    global _global_toast_manager
    return _global_toast_manager

def init_toast_manager(parent):
    """Initialize the global toast manager with a parent widget"""
    global _global_toast_manager
    _global_toast_manager = ToastManager(parent)
    return _global_toast_manager

def show_toast(message, notification_type="info", duration=3000):
    """Show a toast using the global manager"""
    manager = get_toast_manager()
    if manager:
        return manager.show(message, notification_type, duration)
    return None
