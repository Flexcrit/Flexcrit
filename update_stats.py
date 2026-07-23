import urllib.request
import json
import re
import os
import sys

USERNAME = "Flexcrit"

def fetch_repos():
    url = f"https://api.github.com/users/{USERNAME}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Use GITHUB_TOKEN if available to avoid rate-limit errors
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get("public_repos", 0)
    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        return None

def update_readme(repos):
    if repos is None:
        return

    with open("Readme.md", "r") as f:
        content = f.read()

    # Update Repos count using regex
    new_content = re.sub(r"Repos:\s*\.*\s*\d+", f"Repos: ........ {repos}", content)

    if new_content != content:
        with open("Readme.md", "w") as f:
            f.write(new_content)
        print(f"Updated README with {repos} repos.")
    else:
        print("No changes made to README.")

if __name__ == "__main__":
    repos = fetch_repos()
    if repos is None:
        print("Failed to fetch GitHub stats. Exiting.", file=sys.stderr)
        sys.exit(1)
    update_readme(repos)
