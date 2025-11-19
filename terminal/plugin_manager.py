import importlib
import os
import pkgutil
import inspect
from typing import Dict, Any, Callable

class PluginManager:
    def __init__(self, plugin_dir: str = "plugins"):
        # Resolve absolute path relative to this file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.plugin_dir = os.path.join(base_dir, plugin_dir)
        self.commands: Dict[str, Callable] = {}
        self.plugins: Dict[str, Any] = {}
        
        # Create plugins dir if it doesn't exist
        os.makedirs(self.plugin_dir, exist_ok=True)

    def load_plugins(self):
        """Discover and load plugins from the plugins directory."""
        print(f"🔌 Loading plugins from {self.plugin_dir}...")
        
        # Add plugin dir to path so we can import
        import sys
        if self.plugin_dir not in sys.path:
            sys.path.append(self.plugin_dir)

        for _, name, _ in pkgutil.iter_modules([self.plugin_dir]):
            try:
                module = importlib.import_module(name)
                self.plugins[name] = module
                
                # Look for a 'register' function
                if hasattr(module, 'register'):
                    new_commands = module.register()
                    if isinstance(new_commands, dict):
                        self.commands.update(new_commands)
                        print(f"  ✅ Loaded plugin: {name} ({len(new_commands)} commands)")
                else:
                    print(f"  ⚠️  Plugin {name} has no 'register' function")
                    
            except Exception as e:
                print(f"  ❌ Failed to load plugin {name}: {e}")

    def get_command(self, command_name: str) -> Callable:
        return self.commands.get(command_name)

    def list_commands(self) -> Dict[str, str]:
        """Return a dict of command: docstring"""
        return {name: func.__doc__ or "No description" for name, func in self.commands.items()}
