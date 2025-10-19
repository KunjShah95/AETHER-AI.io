"""AetherAI proxy entrypoint.

Lazily imports `terminal.main.main` when invoked so optional runtime
dependencies won't raise import errors at script-install time.
"""

def main(argv=None):
    """Launch the terminal main entrypoint.

    Args:
        argv: Optional list of command-line args (not used). Returns an exit code.
    """
    try:
        from terminal.main import main as _real_main  # local import
    except Exception as e:
        print("AetherAI: failed to import terminal package. Try running from the project root or reinstall.\n")
        print(f"Cause: {e.__class__.__name__}: {e}")
        return 1

    # Delegate to the real main
    return _real_main()

__all__ = ["main"]
"""AetherAI proxy package to expose console entrypoint.

This package provides a stable import path for the console script created
by the editable install. It simply imports and re-exports the main()
callable from the terminal package.
"""
"""Proxy entrypoint for the aetherai console script.

This module lazily imports the heavy `terminal.main` module inside the
`main()` function to avoid raising import errors at console-script startup
when optional dependencies are missing.
"""

def main(argv=None):
    """Launch the terminal main entrypoint.

    Args:
        argv: Optional list of command-line args (not used). Returns an exit code.
    """
    try:
        from terminal.main import main as _real_main  # local import
    except Exception as e:
        print("AetherAI: failed to import terminal package. Try running from the project root or reinstall.\n")
        print(f"Cause: {e.__class__.__name__}: {e}")
        return 1

    # Delegate to the real main
    return _real_main()

__all__ = ["main"]
