import json
import os
from typing import Dict, Optional

class SnippetManager:
    def __init__(self):
        self.snippet_file = os.path.join(os.path.expanduser("~"), ".nexus", "snippets.json")
        self.snippets = self._load_snippets()

    def _load_snippets(self) -> Dict[str, str]:
        if os.path.exists(self.snippet_file):
            try:
                with open(self.snippet_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_snippets(self):
        os.makedirs(os.path.dirname(self.snippet_file), exist_ok=True)
        with open(self.snippet_file, 'w') as f:
            json.dump(self.snippets, f, indent=2)

    def save_snippet(self, name: str, content: str) -> str:
        self.snippets[name] = content
        self._save_snippets()
        return f"✅ Snippet '{name}' saved."

    def get_snippet(self, name: str) -> Optional[str]:
        return self.snippets.get(name)

    def list_snippets(self) -> str:
        if not self.snippets:
            return "No snippets saved."
        return "\n".join(f"- {name}: {content[:50]}..." for name, content in self.snippets.items())

    def delete_snippet(self, name: str) -> str:
        if name in self.snippets:
            del self.snippets[name]
            self._save_snippets()
            return f"✅ Snippet '{name}' deleted."
        return f"❌ Snippet '{name}' not found."
