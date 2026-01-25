"""
NeuroVault Tags Manager
Handles tag parsing, creation, and file-tag associations
"""


class TagsManager:
    """Manager for document tags and categories"""
    
    # Predefined tag colors
    TAG_COLORS = {
        'work': '#3b82f6',      # Blue
        'personal': '#10b981',   # Green
        'important': '#ef4444',  # Red
        'research': '#8b5cf6',   # Purple
        'finance': '#f59e0b',    # Orange
        'health': '#ec4899',     # Pink
        'education': '#06b6d4',  # Cyan
        'travel': '#84cc16',     # Lime
        'default': '#6b7280'     # Gray
    }
    
    def __init__(self):
        pass
    
    def parse_tags(self, tags_string):
        """
        Parse comma-separated tags string into list
        
        Args:
            tags_string: "work, important, 2024"
        
        Returns:
            list: ['work', 'important', '2024']
        """
        if not tags_string or not tags_string.strip():
            return []
        
        tags = []
        for tag in tags_string.split(','):
            # Clean up tag: lowercase, strip whitespace, remove special chars
            cleaned = tag.strip().lower()
            cleaned = ''.join(c for c in cleaned if c.isalnum() or c in '-_ ')
            cleaned = cleaned.strip()
            
            if cleaned and len(cleaned) <= 30:  # Max tag length
                tags.append(cleaned)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_tags = []
        for tag in tags:
            if tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)
        
        return unique_tags[:10]  # Max 10 tags per file
    
    def get_tag_color(self, tag_name):
        """Get color for a tag (use predefined or default)"""
        return self.TAG_COLORS.get(tag_name.lower(), self.TAG_COLORS['default'])
    
    def format_tags_display(self, tags_list):
        """Format tags for display as comma-separated string"""
        return ', '.join(tags_list) if tags_list else ''
    
    def validate_tag(self, tag_name):
        """Check if tag name is valid"""
        if not tag_name or len(tag_name) > 30:
            return False
        # Must be alphanumeric (with spaces/dashes/underscores allowed)
        cleaned = ''.join(c for c in tag_name if c.isalnum() or c in '-_ ')
        return len(cleaned.strip()) > 0


# Global instance
tags_manager = TagsManager()
