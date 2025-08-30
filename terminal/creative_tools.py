#!/usr/bin/env python3
"""
Creative Tools Module for NEXUS AI Terminal
Provides ASCII art, color schemes, music generation, and story creation
"""

import os
import json
import random
import colorsys
from typing import Dict, List, Optional, Tuple
import time

class CreativeTools:
    """Manages creative tools and artistic features"""

    def __init__(self):
        self.ascii_art_db_path = os.path.expanduser("~/.nexus/ascii_art.db")
        self.color_schemes = {}
        self.music_patterns = {}
        self.stories = {}
        self._load_creative_data()
        self._initialize_content()

    def _load_creative_data(self):
        """Load creative tools data"""
        try:
            if os.path.exists(self.ascii_art_db_path):
                with open(self.ascii_art_db_path, 'r') as f:
                    data = json.load(f)
                    self.color_schemes = data.get("color_schemes", {})
        except Exception as e:
            print(f"Warning: Could not load creative database: {e}")

    def _save_creative_data(self):
        """Save creative tools data"""
        try:
            os.makedirs(os.path.dirname(self.ascii_art_db_path), exist_ok=True)
            data = {
                "color_schemes": self.color_schemes,
                "last_updated": time.time()
            }
            with open(self.ascii_art_db_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save creative database: {str(e)}")

    def _initialize_content(self):
        """Initialize creative content"""
        self.ascii_patterns = {
            "big": {
                "A": ["  A  ", " A A ", "AAAAA", "A   A", "A   A"],
                "B": ["BBBB ", "B   B", "BBBB ", "B   B", "BBBB "],
                "C": [" CCC ", "C    ", "C    ", "C    ", " CCC "],
                "D": ["DDD  ", "D  D ", "D   D", "D  D ", "DDD  "],
                "E": ["EEEEE", "E    ", "EEEEE", "E    ", "EEEEE"],
                "F": ["FFFFF", "F    ", "FFFFF", "F    ", "F    "],
                "G": [" GGG ", "G    ", "G GGG", "G   G", " GGG "],
                "H": ["H   H", "H   H", "HHHHH", "H   H", "H   H"],
                "I": [" III ", "  I  ", "  I  ", "  I  ", " III "],
                "J": ["  JJJ", "    J", "    J", "J   J", " JJJ "],
                "K": ["K   K", "K  K ", "KKK  ", "K  K ", "K   K"],
                "L": ["L    ", "L    ", "L    ", "L    ", "LLLLL"],
                "M": ["M   M", "MM MM", "M M M", "M   M", "M   M"],
                "N": ["N   N", "NN  N", "N N N", "N  NN", "N   N"],
                "O": [" OOO ", "O   O", "O   O", "O   O", " OOO "],
                "P": ["PPPP ", "P   P", "PPPP ", "P    ", "P    "],
                "Q": [" QQQ ", "Q   Q", "Q Q Q", "Q  QQ", " QQQQ"],
                "R": ["RRRR ", "R   R", "RRRR ", "R  R ", "R   R"],
                "S": [" SSS ", "S    ", " SSS ", "    S", " SSS "],
                "T": ["TTTTT", "  T  ", "  T  ", "  T  ", "  T  "],
                "U": ["U   U", "U   U", "U   U", "U   U", " UUU "],
                "V": ["V   V", "V   V", "V   V", " V V ", "  V  "],
                "W": ["W   W", "W   W", "W W W", "WW WW", "W   W"],
                "X": ["X   X", " X X ", "  X  ", " X X ", "X   X"],
                "Y": ["Y   Y", " Y Y ", "  Y  ", "  Y  ", "  Y  "],
                "Z": ["ZZZZZ", "   Z ", "  Z  ", " Z   ", "ZZZZZ"]
            },
            "small": {
                "A": ["A", "A", "A", "A", "A"],
                "B": ["B", "B", "B", "B", "B"],
                "C": ["C", "C", "C", "C", "C"],
                "D": ["D", "D", "D", "D", "D"],
                "E": ["E", "E", "E", "E", "E"],
                "F": ["F", "F", "F", "F", "F"],
                "G": ["G", "G", "G", "G", "G"],
                "H": ["H", "H", "H", "H", "H"],
                "I": ["I", "I", "I", "I", "I"],
                "J": ["J", "J", "J", "J", "J"],
                "K": ["K", "K", "K", "K", "K"],
                "L": ["L", "L", "L", "L", "L"],
                "M": ["M", "M", "M", "M", "M"],
                "N": ["N", "N", "N", "N", "N"],
                "O": ["O", "O", "O", "O", "O"],
                "P": ["P", "P", "P", "P", "P"],
                "Q": ["Q", "Q", "Q", "Q", "Q"],
                "R": ["R", "R", "R", "R", "R"],
                "S": ["S", "S", "S", "S", "S"],
                "T": ["T", "T", "T", "T", "T"],
                "U": ["U", "U", "U", "U", "U"],
                "V": ["V", "V", "V", "V", "V"],
                "W": ["W", "W", "W", "W", "W"],
                "X": ["X", "X", "X", "X", "X"],
                "Y": ["Y", "Y", "Y", "Y", "Y"],
                "Z": ["Z", "Z", "Z", "Z", "Z"]
            }
        }

        self.music_scales = {
            "major": [0, 2, 4, 5, 7, 9, 11],
            "minor": [0, 2, 3, 5, 7, 8, 10],
            "pentatonic": [0, 2, 4, 7, 9],
            "blues": [0, 3, 5, 6, 7, 10]
        }

        self.story_templates = {
            "fantasy": {
                "settings": ["enchanted forest", "ancient castle", "mystical mountain", "hidden valley"],
                "characters": ["brave knight", "wise wizard", "mysterious elf", "courageous peasant"],
                "conflicts": ["evil sorcerer", "ancient curse", "lost treasure", "dark prophecy"],
                "resolutions": ["heroic battle", "magical spell", "ancient wisdom", "unexpected alliance"]
            },
            "scifi": {
                "settings": ["distant planet", "space station", "cyberpunk city", "time vortex"],
                "characters": ["brave captain", "brilliant scientist", "rogue hacker", "alien diplomat"],
                "conflicts": ["alien invasion", "time paradox", "AI rebellion", "cosmic disaster"],
                "resolutions": ["technological breakthrough", "diplomatic solution", "heroic sacrifice", "quantum leap"]
            },
            "mystery": {
                "settings": ["old mansion", "foggy harbor", "abandoned warehouse", "quiet village"],
                "characters": ["sharp detective", "mysterious informant", "suspicious butler", "innocent bystander"],
                "conflicts": ["missing person", "stolen artifact", "corporate espionage", "family secret"],
                "resolutions": ["clever deduction", "surprising twist", "hidden evidence", "confession"]
            }
        }

    def generate_ascii_art(self, text: str, style: str = "big") -> str:
        """Generate ASCII art from text"""
        try:
            text = text.upper()
            if style not in self.ascii_patterns:
                return f"❌ Style '{style}' not found. Available: {', '.join(self.ascii_patterns.keys())}"

            pattern = self.ascii_patterns[style]
            lines = [""] * 5  # 5 lines for big style

            for char in text:
                if char == " ":
                    # Add space between characters
                    for i in range(5):
                        lines[i] += "  "
                elif char in pattern:
                    char_pattern = pattern[char]
                    for i in range(min(len(lines), len(char_pattern))):
                        lines[i] += char_pattern[i] + " "
                else:
                    # Unknown character - add space
                    for i in range(5):
                        lines[i] += "  "

            return "\n".join(lines)

        except Exception as e:
            return f"❌ Failed to generate ASCII art: {str(e)}"

    def generate_color_scheme(self, base_color: str = None, scheme_type: str = "complementary") -> Dict:
        """Generate a color scheme"""
        try:
            # Parse base color or generate random
            if base_color:
                # Simple hex color parsing
                if base_color.startswith("#"):
                    base_color = base_color[1:]
                r = int(base_color[:2], 16) / 255.0
                g = int(base_color[2:4], 16) / 255.0
                b = int(base_color[4:6], 16) / 255.0
            else:
                # Generate random vibrant color
                h = random.random()
                s = 0.7 + random.random() * 0.3
                v = 0.8 + random.random() * 0.2
                r, g, b = colorsys.hsv_to_rgb(h, s, v)

            h, s, v = colorsys.rgb_to_hsv(r, g, b)

            scheme = {
                "base_color": f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}",
                "colors": [],
                "type": scheme_type
            }

            if scheme_type == "complementary":
                # Complementary color (opposite on color wheel)
                comp_h = (h + 0.5) % 1.0
                comp_r, comp_g, comp_b = colorsys.hsv_to_rgb(comp_h, s, v)
                scheme["colors"] = [
                    f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}",
                    f"#{int(comp_r*255):02x}{int(comp_g*255):02x}{int(comp_b*255):02x}"
                ]

            elif scheme_type == "triadic":
                # Triadic colors (120 degrees apart)
                h1 = (h + 1/3) % 1.0
                h2 = (h + 2/3) % 1.0
                r1, g1, b1 = colorsys.hsv_to_rgb(h1, s, v)
                r2, g2, b2 = colorsys.hsv_to_rgb(h2, s, v)
                scheme["colors"] = [
                    f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}",
                    f"#{int(r1*255):02x}{int(g1*255):02x}{int(b1*255):02x}",
                    f"#{int(r2*255):02x}{int(g2*255):02x}{int(b2*255):02x}"
                ]

            elif scheme_type == "analogous":
                # Analogous colors (adjacent on color wheel)
                h1 = (h + 0.083) % 1.0  # +30 degrees
                h2 = (h - 0.083) % 1.0  # -30 degrees
                r1, g1, b1 = colorsys.hsv_to_rgb(h1, s, v)
                r2, g2, b2 = colorsys.hsv_to_rgb(h2, s, v)
                scheme["colors"] = [
                    f"#{int(r2*255):02x}{int(g2*255):02x}{int(b2*255):02x}",
                    f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}",
                    f"#{int(r1*255):02x}{int(g1*255):02x}{int(b1*255):02x}"
                ]

            elif scheme_type == "monochromatic":
                # Monochromatic (different shades of same color)
                shades = []
                for i in range(5):
                    new_v = max(0.2, min(0.9, v - 0.15 * (i - 2)))
                    shade_r, shade_g, shade_b = colorsys.hsv_to_rgb(h, s, new_v)
                    shades.append(f"#{int(shade_r*255):02x}{int(shade_g*255):02x}{int(shade_b*255):02x}")
                scheme["colors"] = shades

            # Save the scheme
            scheme_id = f"scheme_{int(time.time())}_{random.randint(1000, 9999)}"
            self.color_schemes[scheme_id] = scheme
            self._save_creative_data()

            return scheme

        except Exception as e:
            return {"error": f"Failed to generate color scheme: {str(e)}"}

    def generate_music(self, mood: str = "happy", length: int = 8) -> Dict:
        """Generate simple musical melody"""
        try:
            # Note frequencies (in Hz) for a basic scale
            note_freqs = {
                'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
                'G4': 392.00, 'A4': 440.00, 'B4': 493.88, 'C5': 523.25
            }

            notes = list(note_freqs.keys())

            # Mood-based patterns
            mood_patterns = {
                "happy": ["C4", "E4", "G4", "C5", "G4", "E4", "C4"],
                "sad": ["C4", "A4", "F4", "C4", "F4", "A4", "C4"],
                "mysterious": ["C4", "F4", "G4", "A4", "G4", "F4", "C4"],
                "energetic": ["C4", "G4", "E4", "C4", "G4", "E4", "C4"]
            }

            if mood not in mood_patterns:
                mood = random.choice(list(mood_patterns.keys()))

            pattern = mood_patterns[mood]

            # Generate melody
            melody = []
            for i in range(length):
                if i < len(pattern):
                    note = pattern[i % len(pattern)]
                else:
                    note = random.choice(notes)

                duration = random.choice([0.25, 0.5, 1.0])  # quarter, half, whole notes
                melody.append({
                    "note": note,
                    "frequency": note_freqs.get(note, 261.63),
                    "duration": duration,
                    "position": i
                })

            return {
                "mood": mood,
                "length": length,
                "melody": melody,
                "notation": " ".join([note["note"] for note in melody]),
                "description": f"A {mood} melody with {length} notes"
            }

        except Exception as e:
            return {"error": f"Failed to generate music: {str(e)}"}

    def generate_story(self, genre: str = "fantasy", length: str = "short") -> Dict:
        """Generate a creative story"""
        try:
            if genre not in self.story_templates:
                genre = random.choice(list(self.story_templates.keys()))

            template = self.story_templates[genre]

            # Generate story elements
            setting = random.choice(template["settings"])
            character = random.choice(template["characters"])
            conflict = random.choice(template["conflicts"])
            resolution = random.choice(template["resolutions"])

            # Create story based on length
            if length == "short":
                story = f"In a {setting}, a {character} faced a great challenge: {conflict}. Through courage and wit, they achieved {resolution}, bringing peace to all."
            elif length == "medium":
                story = f"""Once upon a time in a {setting}, there lived a {character} who was known throughout the land for their remarkable abilities.

One day, a terrible {conflict} threatened everything they held dear. Undeterred, the {character.split()[1]} embarked on a perilous journey to confront this danger.

After many trials and tribulations, they discovered that the key to victory lay in {resolution}. With this knowledge, they overcame the challenge and restored balance to their world.

The {character.split()[1]} became a legend, remembered forever for their bravery and wisdom."""
            else:  # long
                story = f"""In the heart of a {setting}, there dwelled a {character} named Alex. Life had been peaceful until the day when {conflict} began to unfold.

Alex, sensing the danger, knew they had to act. Gathering their courage, they set out on a quest that would test the limits of their abilities and change them forever.

Along the way, Alex encountered many challenges and made both friends and enemies. They learned valuable lessons about trust, perseverance, and the true meaning of heroism.

Finally, through a combination of clever strategy and {resolution}, Alex was able to overcome the great threat. The {setting} was saved, and Alex returned home transformed, ready to face whatever adventures the future might bring.

Their story became the stuff of legends, inspiring generations to come."""

            return {
                "genre": genre,
                "length": length,
                "title": f"The {character.split()[1].title()}'s {genre.title()} Adventure",
                "story": story,
                "elements": {
                    "setting": setting,
                    "character": character,
                    "conflict": conflict,
                    "resolution": resolution
                }
            }

        except Exception as e:
            return {"error": f"Failed to generate story: {str(e)}"}

    def get_available_themes(self) -> Dict:
        """Get available creative themes and options"""
        return {
            "ascii_styles": list(self.ascii_patterns.keys()),
            "color_schemes": ["complementary", "triadic", "analogous", "monochromatic"],
            "music_moods": list(self.music_scales.keys()),
            "story_genres": list(self.story_templates.keys()),
            "story_lengths": ["short", "medium", "long"]
        }

    def save_color_scheme(self, scheme_id: str, name: str) -> str:
        """Save a color scheme with a custom name"""
        try:
            if scheme_id not in self.color_schemes:
                return "❌ Color scheme not found"

            self.color_schemes[scheme_id]["name"] = name
            self._save_creative_data()

            return f"✅ Color scheme saved as '{name}'"

        except Exception as e:
            return f"❌ Failed to save color scheme: {str(e)}"

    def list_color_schemes(self) -> List[Dict]:
        """List saved color schemes"""
        try:
            schemes = []
            for scheme_id, scheme in self.color_schemes.items():
                schemes.append({
                    "id": scheme_id,
                    "name": scheme.get("name", f"Scheme {scheme_id}"),
                    "type": scheme.get("type", "unknown"),
                    "colors": scheme.get("colors", []),
                    "base_color": scheme.get("base_color", "#000000")
                })

            return schemes

        except Exception as e:
            return [{"error": f"Failed to list color schemes: {str(e)}"}]