import re

with open("ref/arsa-branding-inventory.md", "r") as f:
    inventory = f.read()

with open("ref/arsa-branding-summary.md", "r") as f:
    summary = f.read()

import subprocess
# Run exhaustive search
cmd = 'find . -type f -not -path "*/\.git/*" -not -path "*/node_modules/*" -not -path "*/\.svelte-kit/*" -not -path "*/build/*" -not -path "*/dist/*" -not -path "*/__pycache__/*" -not -path "*/\.venv/*" -not -path "*/venv/*" -not -path "*/\.pytest_cache/*" -not -name "*.log" -not -name "package-lock.json" -not -name "yarn.lock" -not -name "pnpm-lock.yaml" -exec grep -ilE "open[ -]*webui" {} +'
out = subprocess.check_output(cmd, shell=True, text=True)

files = [line.strip().lstrip('./') for line in out.split('\n') if line.strip()]

unlisted_files = []
for file in files:
    # Check if the filename exists in inventory or summary
    if file not in inventory and file not in summary:
        # Ignore dot files or CI stuff for now, or just list them all
        unlisted_files.append(file)

print("Files found in exhaustive search but NOT listed in reference documents:")
for f in unlisted_files:
    print(f"- {f}")
