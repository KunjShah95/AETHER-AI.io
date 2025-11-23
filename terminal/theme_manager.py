"""
NEXUS AI Terminal - Customizable UI Themes
Provides beautiful, customizable color themes for the terminal interface
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

class ThemeManager:
    """Manages customizable UI themes for the NEXUS AI Terminal"""

    def __init__(self, themes_file: str = "themes.json"):
        self.themes_file = themes_file
        self.current_theme = "dark"
        self.themes = self._load_default_themes()
        self._load_custom_themes()

    def _load_default_themes(self) -> Dict:
        """Load the default built-in themes"""
        return {
            "dark": {
                "name": "Dark Professional",
                "description": "Clean dark theme with professional colors",
                "colors": {
                    "primary": "#00ff88",
                    "secondary": "#0088ff",
                    "accent": "#ff6b6b",
                    "success": "#51cf66",
                    "warning": "#ffd43b",
                    "error": "#ff6b6b",
                    "info": "#74c0fc",
                    "text": "#ffffff",
                    "text_secondary": "#cccccc",
                    "background": "#1a1a1a",
                    "panel_bg": "#2d2d2d",
                    "border": "#404040",
                    "highlight": "#333333"
                },
                "icons": {
                    "success": "✅",
                    "error": "❌",
                    "warning": "⚠️",
                    "info": "ℹ️",
                    "loading": "⏳",
                    "complete": "✅",
                    "arrow": "➤",
                    "bullet": "•"
                }
            },
            "light": {
                "name": "Light Professional",
                "description": "Clean light theme with professional colors",
                "colors": {
                    "primary": "#2e7d32",
                    "secondary": "#1976d2",
                    "accent": "#d32f2f",
                    "success": "#388e3c",
                    "warning": "#f57c00",
                    "error": "#d32f2f",
                    "info": "#0288d1",
                    "text": "#212121",
                    "text_secondary": "#757575",
                    "background": "#ffffff",
                    "panel_bg": "#f5f5f5",
                    "border": "#e0e0e0",
                    "highlight": "#eeeeee"
                },
                "icons": {
                    "success": "✅",
                    "error": "❌",
                    "warning": "⚠️",
                    "info": "ℹ️",
                    "loading": "⏳",
                    "complete": "✅",
                    "arrow": "➤",
                    "bullet": "•"
                }
            },
            "neon": {
                "name": "Neon Cyberpunk",
                "description": "Vibrant neon colors for a cyberpunk aesthetic",
                "colors": {
                    "primary": "#00ffff",
                    "secondary": "#ff00ff",
                    "accent": "#ffff00",
                    "success": "#00ff00",
                    "warning": "#ffaa00",
                    "error": "#ff0040",
                    "info": "#0080ff",
                    "text": "#ffffff",
                    "text_secondary": "#cccccc",
                    "background": "#0a0a0a",
                    "panel_bg": "#1a1a1a",
                    "border": "#333333",
                    "highlight": "#2a2a2a"
                },
                "icons": {
                    "success": "💚",
                    "error": "💔",
                    "warning": "⚡",
                    "info": "🔵",
                    "loading": "🌟",
                    "complete": "✨",
                    "arrow": "▶",
                    "bullet": "◆"
                }
            },
            "ocean": {
                "name": "Ocean Blue",
                "description": "Calming blue ocean-inspired theme",
                "colors": {
                    "primary": "#00bcd4",
                    "secondary": "#2196f3",
                    "accent": "#ff9800",
                    "success": "#4caf50",
                    "warning": "#ff9800",
                    "error": "#f44336",
                    "info": "#03a9f4",
                    "text": "#212121",
                    "text_secondary": "#757575",
                    "background": "#e3f2fd",
                    "panel_bg": "#ffffff",
                    "border": "#bbdefb",
                    "highlight": "#f1f8e9"
                },
                "icons": {
                    "success": "🌊",
                    "error": "🌋",
                    "warning": "🌤️",
                    "info": "💧",
                    "loading": "🌊",
                    "complete": "🏄",
                    "arrow": "➤",
                    "bullet": "○"
                }
            },
            "forest": {
                "name": "Forest Green",
                "description": "Natural forest-inspired green theme",
                "colors": {
                    "primary": "#4caf50",
                    "secondary": "#8bc34a",
                    "accent": "#ff5722",
                    "success": "#388e3c",
                    "warning": "#ff9800",
                    "error": "#f44336",
                    "info": "#2196f3",
                    "text": "#212121",
                    "text_secondary": "#757575",
                    "background": "#f1f8e9",
                    "panel_bg": "#ffffff",
                    "border": "#c8e6c9",
                    "highlight": "#e8f5e8"
                },
                "icons": {
                    "success": "🌿",
                    "error": "🍂",
                    "warning": "🌳",
                    "info": "🌱",
                    "loading": "🌲",
                    "complete": "🌳",
                    "arrow": "➤",
                    "bullet": "●"
                }
            },
            "sunset": {
                "name": "Sunset Orange",
                "description": "Warm sunset-inspired orange theme",
                "colors": {
                    "primary": "#ff5722",
                    "secondary": "#ff9800",
                    "accent": "#9c27b0",
                    "success": "#4caf50",
                    "warning": "#ff9800",
                    "error": "#f44336",
                    "info": "#2196f3",
                    "text": "#212121",
                    "text_secondary": "#757575",
                    "background": "#fff3e0",
                    "panel_bg": "#ffffff",
                    "border": "#ffcc02",
                    "highlight": "#ffe0b2"
                },
                "icons": {
                    "success": "🌅",
                    "error": "🌋",
                    "warning": "🌇",
                    "info": "🌞",
                    "loading": "🌄",
                    "complete": "🌅",
                    "arrow": "➤",
                    "bullet": "●"
                }
            },
            "matrix": {
                "name": "The Matrix",
                "description": "Digital rain inspired theme",
                "colors": {
                    "primary": "#00ff00",
                    "secondary": "#008f11",
                    "accent": "#003b00",
                    "success": "#00ff00",
                    "warning": "#ffff00",
                    "error": "#ff0000",
                    "info": "#00cc00",
                    "text": "#00ff00",
                    "text_secondary": "#008f11",
                    "background": "#000000",
                    "panel_bg": "#020202",
                    "border": "#003300",
                    "highlight": "#001100"
                },
                "icons": {
                    "success": "[OK]",
                    "error": "[ERR]",
                    "warning": "[!]",
                    "info": "[i]",
                    "loading": "...",
                    "complete": "[DONE]",
                    "arrow": ">",
                    "bullet": "*"
                }
            },
            "hacker": {
                "name": "Cyber Security",
                "description": "High contrast terminal theme",
                "colors": {
                    "primary": "#ff00ff",
                    "secondary": "#00ffff",
                    "accent": "#ffff00",
                    "success": "#00ff00",
                    "warning": "#ff0000",
                    "error": "#ff0000",
                    "info": "#0000ff",
                    "text": "#ffffff",
                    "text_secondary": "#aaaaaa",
                    "background": "#000000",
                    "panel_bg": "#111111",
                    "border": "#ffffff",
                    "highlight": "#222222"
                },
                "icons": {
                    "success": "+",
                    "error": "x",
                    "warning": "!",
                    "info": "?",
                    "loading": "/",
                    "complete": "#",
                    "arrow": ">>",
                    "bullet": "-"
                }
            }
        }

    def _load_custom_themes(self):
        """Load custom themes from file"""
        if os.path.exists(self.themes_file):
            try:
                with open(self.themes_file, 'r') as f:
                    custom_themes = json.load(f)
                    self.themes.update(custom_themes)
            except Exception as e:
                print(f"Warning: Could not load custom themes: {e}")

    def _save_custom_themes(self):
        """Save custom themes to file"""
        custom_themes = {k: v for k, v in self.themes.items() if k not in self._load_default_themes()}
        try:
            with open(self.themes_file, 'w') as f:
                json.dump(custom_themes, f, indent=2)
        except Exception as e:
            return f"❌ Error saving custom themes: {e}"
        return "✅ Custom themes saved successfully"

    def get_theme(self, theme_name: str) -> Optional[Dict]:
        """Get a theme by name"""
        return self.themes.get(theme_name)

    def set_current_theme(self, theme_name: str) -> str:
        """Set the current active theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            return f"✅ Theme switched to: {self.themes[theme_name]['name']}"
        else:
            return f"❌ Theme '{theme_name}' not found. Available themes: {', '.join(self.themes.keys())}"

    def get_current_theme(self) -> Dict:
        """Get the current active theme"""
        return self.themes.get(self.current_theme, self.themes["dark"])

    def list_themes(self) -> str:
        """List all available themes"""
        output = "🎨 Available Themes:\n\n"
        for name, theme in self.themes.items():
            current_marker = " ← Current" if name == self.current_theme else ""
            output += f"• {name}: {theme['name']} - {theme['description']}{current_marker}\n"
        return output

    def create_custom_theme(self, name: str, base_theme: str = "dark", **customizations) -> str:
        """Create a custom theme based on an existing theme"""
        if base_theme not in self.themes:
            return f"❌ Base theme '{base_theme}' not found"

        if name in self.themes:
            return f"❌ Theme '{name}' already exists"

        # Create new theme based on base theme
        new_theme = self.themes[base_theme].copy()
        new_theme["name"] = customizations.get("name", f"Custom {name.title()}")
        new_theme["description"] = customizations.get("description", f"Custom theme based on {base_theme}")

        # Apply customizations
        if "colors" in customizations:
            new_theme["colors"].update(customizations["colors"])
        if "icons" in customizations:
            new_theme["icons"].update(customizations["icons"])

        self.themes[name] = new_theme
        self._save_custom_themes()
        return f"✅ Custom theme '{name}' created successfully"

    def delete_custom_theme(self, name: str) -> str:
        """Delete a custom theme"""
        if name not in self.themes:
            return f"❌ Theme '{name}' not found"

        if name in self._load_default_themes():
            return f"❌ Cannot delete built-in theme '{name}'"

        del self.themes[name]
        self._save_custom_themes()
        return f"✅ Custom theme '{name}' deleted successfully"

    def get_rich_theme(self) -> Theme:
        """Get Rich theme object for current theme"""
        theme = self.get_current_theme()
        colors = theme["colors"]

        return Theme({
            "primary": colors["primary"],
            "secondary": colors["secondary"],
            "accent": colors["accent"],
            "success": colors["success"],
            "warning": colors["warning"],
            "error": colors["error"],
            "info": colors["info"],
            "text": colors["text"],
            "text_secondary": colors["text_secondary"],
            "background": colors["background"],
            "panel_bg": colors["panel_bg"],
            "border": colors["border"],
            "highlight": colors["highlight"]
        })

    def preview_theme(self, theme_name: str) -> str:
        """Generate a preview of a theme"""
        if theme_name not in self.themes:
            return f"❌ Theme '{theme_name}' not found"

        theme = self.themes[theme_name]
        colors = theme["colors"]
        icons = theme["icons"]

        preview = f"""
🎨 Theme Preview: {theme['name']}
{theme['description']}

Colors:
• Primary: {colors['primary']}
• Secondary: {colors['secondary']}
• Accent: {colors['accent']}
• Success: {colors['success']}
• Warning: {colors['warning']}
• Error: {colors['error']}
• Info: {colors['info']}

Icons:
• Success: {icons['success']}
• Error: {icons['error']}
• Warning: {icons['warning']}
• Info: {icons['info']}
• Loading: {icons['loading']}
• Complete: {icons['complete']}
• Arrow: {icons['arrow']}
• Bullet: {icons['bullet']}
"""
        return preview

    def export_theme(self, theme_name: str, format_type: str = "json") -> str:
        """Export a theme configuration"""
        if theme_name not in self.themes:
            return f"❌ Theme '{theme_name}' not found"

        theme = self.themes[theme_name]

        if format_type.lower() == "json":
            return json.dumps(theme, indent=2)
        elif format_type.lower() == "python":
            return f"""# {theme['name']} Theme Configuration
THEME_{theme_name.upper()} = {json.dumps(theme, indent=4)}
"""
        else:
            return f"❌ Unsupported export format: {format_type}. Use 'json' or 'python'"

    def get_theme_stats(self) -> str:
        """Get statistics about themes"""
        total_themes = len(self.themes)
        default_themes = len(self._load_default_themes())
        custom_themes = total_themes - default_themes

        stats = f"""
📊 Theme Statistics:
• Total Themes: {total_themes}
• Built-in Themes: {default_themes}
• Custom Themes: {custom_themes}
• Current Theme: {self.current_theme} ({self.themes[self.current_theme]['name']})
"""
        return stats

    def reset_to_default(self) -> str:
        """Reset to default dark theme"""
        self.current_theme = "dark"
        return "✅ Reset to default Dark Professional theme"

    def get_startup_animation(self) -> List[str]:
        """Get frames for startup animation"""
        return [
            "Initializing NEXUS AI...",
            "Loading modules...",
            "Connecting to neural network...",
            "Establishing secure link...",
            "System ready."
        ]
