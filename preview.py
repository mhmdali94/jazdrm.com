#!/usr/bin/env python3
"""
Lightweight Static Server for jazdrm.com offline clone.
Opens browser automatically at http://localhost:8080.
"""

import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8080
DIRECTORY = Path(__file__).resolve().parent

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

if __name__ == "__main__":
    print(f"Starting Jazdrm.com static server at http://localhost:{PORT}")
    print("Press Ctrl+C to stop.")
    try:
        webbrowser.open(f"http://localhost:{PORT}")
    except Exception:
        pass
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
