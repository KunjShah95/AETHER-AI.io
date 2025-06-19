#!/usr/bin/env python3
"""
Simple HTTP server for the NEXUS AI website
"""

import http.server
import socketserver
import os
import webbrowser

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class NexusHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()


def main():
    try:
        # Change to the directory of the script
        os.chdir(DIRECTORY)  # Create the server
        with socketserver.TCPServer(("", PORT), NexusHTTPRequestHandler) as httpd:
            url = "http://localhost:{}/index.html".format(PORT)

            print("=" * 60)
            print("🚀 NEXUS AI Website Server")
            print("=" * 60)
            print("✅ Server started at: http://localhost:{}".format(PORT))
            print("📂 Serving from: {}".format(DIRECTORY))
            print("🌐 Open this URL in your browser: {}".format(url))
            print("=" * 60)
            print("Press Ctrl+C to stop the server")

            # Open the browser automatically
            webbrowser.open(url)

            # Start the server
            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print("\n❌ Error: {}".format(e))


if __name__ == "__main__":
    main()
