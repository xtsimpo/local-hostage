#!/usr/bin/env python3
"""
Updates the CSP hash of the main script inside vault.html.

vault.html only allows its OWN script to run (script-src 'sha256-...').
If you change even one character of that script, run:

    python3 build.py

otherwise the browser will block the script and you will see a blank page.
"""
import base64
import hashlib
import pathlib
import re
import sys

path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "vault.html")
src = path.read_text(encoding="utf-8").replace("\r\n", "\n")

scripts = re.findall(r"<script>(.*?)</script>", src, re.S)
if len(scripts) != 1:
    sys.exit(f"Expected exactly one <script> without attributes, found {len(scripts)}.")

digest = base64.b64encode(hashlib.sha256(scripts[0].encode("utf-8")).digest()).decode()
out, n = re.subn(r"script-src 'sha256-[^']*'", f"script-src 'sha256-{digest}'", src)
if n != 1:
    sys.exit("Could not find script-src in the Content-Security-Policy.")

data = re.search(r'<script[^>]*id="vault-data"[^>]*>(.*?)</script>', out, re.S)
if data and data.group(1).strip() != "null":
    print("Warning: this file contains a vault. Do not commit it.", file=sys.stderr)

path.write_text(out, encoding="utf-8", newline="\n")
print(f"OK  sha256-{digest}")
