
import subprocess
import sys
import os

def check_ollama():
    print("🔍 Diagnosing Ollama Configuration...")
    
    # 1. Check if 'ollama' is in PATH
    print("\n1. Checking Ollama CLI...")
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama CLI found: {result.stdout.strip()}")
        else:
            print(f"❌ Ollama CLI found but returned error: {result.stderr}")
    except FileNotFoundError:
        print("❌ Ollama CLI not found in PATH.")
        print("   Please install Ollama from https://ollama.com/download")
        return

    # 2. Check if Ollama service is running (by listing models)
    print("\n2. Checking Ollama Service (listing models)...")
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama Service is running.")
            lines = result.stdout.strip().splitlines()
            if len(lines) > 1:
                print(f"   Found {len(lines)-1} models:")
                for line in lines:
                    print(f"   - {line}")
            else:
                print("   ⚠️ No models found. Run 'ollama pull llama3' to get a model.")
        else:
            print(f"❌ Ollama Service check failed: {result.stderr}")
            print("   Make sure the Ollama app is running in the background.")
    except Exception as e:
        print(f"❌ Error checking service: {e}")

    # 3. Check Python Library
    print("\n3. Checking Python 'ollama' library...")
    try:
        import ollama
        print(f"✅ Python 'ollama' library imported (version: {ollama.__version__ if hasattr(ollama, '__version__') else 'unknown'})")
        try:
            models = ollama.list()
            print("✅ Python client successfully connected to Ollama.")
        except Exception as e:
            print(f"❌ Python client failed to connect: {e}")
    except ImportError:
        print("❌ Python 'ollama' library not installed.")
        print("   Run: pip install ollama")

if __name__ == "__main__":
    check_ollama()
