import sys
import os

def check_import(module_name, feature_name):
    try:
        __import__(module_name)
        print(f"✅ {feature_name} module loaded successfully.")
        return True
    except ImportError as e:
        print(f"❌ {feature_name} module failed to load: {e}")
        return False
    except Exception as e:
        print(f"❌ {feature_name} module error: {e}")
        return False

print("🔍 Verifying Nexus AI Feature Installation...\n")

features = [
    ("terminal.docker_manager", "Docker Manager"),
    ("terminal.rag", "RAG Manager"),
    ("terminal.dashboard_tui", "TUI Dashboard"),
    ("terminal.plugin_manager", "Plugin Manager"),
    ("terminal.snippet_manager", "Snippet Manager"),
    ("terminal.web_admin", "Web Admin"),
    ("terminal.persona_manager", "Persona Manager"),
    ("terminal.network_tools", "Network Tools"),
    ("terminal.voice", "Voice Manager")
]

success = True
for module, name in features:
    if not check_import(module, name):
        success = False

print("\n" + ("="*50))
if success:
    print("🎉 All new features are correctly installed and importable!")
    print("You can now run the terminal with: python terminal/main.py")
else:
    print("⚠️ Some features have missing dependencies or errors.")
    print("Please run: pip install -r terminal/requirements.txt")
print("="*50)
